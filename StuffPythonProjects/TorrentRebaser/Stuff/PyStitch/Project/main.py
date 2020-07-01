import pandas as pd
import glob
import calendar
import datetime

class CSV_Combiner:
    def __init__(self):
        self.trading_days_in_deep = 5
        # Cycle through all of the files in the folder and find the last date listed in the file.
        # The last listed date in each .csv file represents the contract closing date
        # Next make a list with the file name and last recorded date of each file
        # list structure: dates=[[file_name,last_date,last_time]]
        files = []
        file_end = '*.csv'
        for fname in glob.glob(file_end):
            # Will skip generated file, we suppose that market data files does not contain "_full_" and our result file does
            if "_full_" not in fname:
                files.append(fname)
                # add a header to the file, only if there is no header
                self.add_header(fname)

        # get the last date and time (first row) of each file
        # this will be used to determine the date ranges to slice from each file
        file_date_time = []
        data_frames = []
        for file in files:
            data_frames.append(self.load_data_frame_from_file_with_split_to_five_days_before(file))
            date, time = self.last_date(file)
            file_date_time.append([file, date, time])

        final_data = pd.DataFrame([])

        for i in range(len(data_frames)):
            main_frame = data_frames[i][0]
            main_frame['DateTime'] = main_frame['Date'] + " " + main_frame['Time']
            # If we should manage previous period's last five days
            #if not five_days_frame is None:
            #    for record in five_days_frame:
    #        #        if record.Date in main_frame.Date and record.Time in main_frame.Time:
            #            print('Oga oga')
            five_days_frame = data_frames[i][1]
            five_days_frame['DateTime'] = five_days_frame['Date'] + " " + five_days_frame['Time']
            b = main_frame.set_index('DateTime').add(five_days_frame.set_index('DateTime')).reset_index()
            b.drop(columns="DateTime")

            for (j, row) in five_days_frame.iterrows():
                val = row['DateTime']
                if main_frame.__contains__(val):
                    vol = row['Volume']
                    row['Volume'] += 1

            result = pd.merge(main_frame, five_days_frame, on=['DateTime'])
            a = "aaa"
            #result = pd.merge(main_frame, five_days_frame[['Adj Vol', 'Volume']], on=['DateTime'])
            #final_data = appendDataFrame(final_data, b)

        self.save_to_csv(final_data, "Final_full_data.csv")

        # sort the files by date
        file_date_time2 = sorted(file_date_time, key=lambda file: file[1])

        # for file in file_date_time2:
        # print(file)
        # return

        # create a list of the date/time periods to slice from each file
        # format: [[file_name,start_date,start_time,end_date,end_time]]

        slice_list = list()#[['ESH18_12_01_to_03_30.csv', '2007-12-20', '09:31:00', '2008-03-20', '09:30:00']]
        for i in range(0, len(file_date_time2)):
            file_name = file_date_time2[i][0]
            # go into the previous file and find the date/time closest to the previous end date/time
            # first get the end date/time from the previous month
            if i > 0:
                start_date, start_time_test = file_date_time2[i - 1][1], file_date_time2[i - 1][2]
                # next look in current month file and get the first time that is later than the end time of the previous month file
                start_time = self.get_time(file_date_time2[i][0], start_date, start_time_test)
                # end date is good
            else:
                start_date, start_time = self.first_date(file_date_time2[i][0])#[1], file_date_time2[i - 1][2]
            end_date, end_time = file_date_time2[i][1], file_date_time2[i][2]
            slice_list.append([file_name, start_date, start_time, end_date, end_time])

        # reverse the order of slice_list
        slice_list.reverse()

        # Next we want to iterate backwards through the list of files and pull the section in each range given
        # and attach that to the end of a new dataframe we are creating.

        full_data = pd.DataFrame([])

        for i in range(len(slice_list)):
            # print(slice_list[i])
            df = pd.read_csv(slice_list[i][0], header=0)
            # get the index of the top of the slice. Should always be idx = 0
            top_idx_df1 = df.loc[df['Date'] == slice_list[i][3]]
            top_idx_t = top_idx_df1.index[top_idx_df1['Time'] == slice_list[i][4]].tolist()
            top_idx = top_idx_t[0]
            # print('top_idx = '+str(top_idx)+' df = ')
            # print(df.loc[top_idx][['Date','Time']])

            # next get the index of the end of the slice
            low_idx_df1 = df.loc[df['Date'] == slice_list[i][1]]
            low_idx_t = low_idx_df1.index[low_idx_df1['Time'] == slice_list[i][2]].tolist()
            low_idx = low_idx_t[0]
            # print('low_idx = '+str(low_idx)+' df = ')
            # print(df.loc[low_idx][['Date','Time']])

            # create dataframe based on given indexes
            final_df = df.loc[top_idx:low_idx]
            # append to overall df
            full_data = full_data.append(final_df)
            print("i = {}".format(i))

        # if i > 2:
        # break

        # Finally save the compiled data to a new .csv file
        # save_to_csv(full_data)
        print('Total rows in final data set: ' + str(full_data.shape[0]))
        start_month_number = calendar.month_abbr[int(slice_list[-1][1].split("-")[1])]
        start_year = slice_list[-1][1].split("-")[0]
        end_month_number = calendar.month_abbr[int(slice_list[0][1].split("-")[1])]
        end_year = slice_list[0][1].split("-")[0]
        filename = 'ES_full_'+start_month_number+'_'+start_year+'_to_'+end_month_number+'_'+end_year+'.csv'
        self.save_to_csv(full_data, filename)


    # df_samp=full_data.iloc[::1000, :]
    # print(df_samp[['Date','Time']])
    # save_to_csv(df_samp,'all_data.csv')

    # open csv file, return the data in a pandas dataframe
    def import_data(self, file_name):
        # open the file using pandas, use the first row as the header
        data = pd.read_csv(file_name, header=0)
        return data

    def count_rows(self, file_name):
        with open(file_name) as f:
            return sum(1 for line in f)

    def add_header(self, file_name):
        header = 'Date,Time,Adj Vol,Volume,Open,High,Low,Close\n'
        # Note need to check this is the right order for the header

        with open(file_name, 'r') as original:
            data = original.read()

        # Split file into parts with delimeter equal to header. If file already contains header - result wold consist of
        #  few elements, first one is empty and then we just ignore adding
        if data.split(header)[0] != '':
            with open(file_name, 'w') as outfile:
                outfile.write(header + data)

    def last_date(self, file_name):
        # This function outputs the date/time of the top row in the csv file
        df = pd.read_csv(file_name, header=0)
        out_time = [x for x in list(df.Time) if x != 'Time']
        out_date = [x for x in list(df.Date) if x != 'Date']
        return out_date[0], out_time[0]

    def first_date(self, file_name):
        # This function outputs the date/time of the bottom row in the csv file
        df = pd.read_csv(file_name, header=0)
        out_time = [x for x in list(df.Time) if x != 'Time']
        out_date = [x for x in list(df.Date) if x != 'Date']
        return out_date[-1], out_time[-1]

    def get_time(self, file_name, date, time):
        # go into the file, for the given date, pull out the first time
        # that is later than the given time
        df = pd.read_csv(file_name, header=0)
        time_idx_df = df.loc[df['Date'] == date]
        # print(time_idx_df[['Date','Time']])
        time_idx = time_idx_df.index[time_idx_df['Time'] > time].tolist()
        # print(time_idx)
        out_time_idx = time_idx[-1]
        out_time = df.loc[[out_time_idx], ['Time']].values.tolist()
        # print(out_time[0][0])
        return out_time[0][0]

    def remove_rows(self, file):
        data = ''
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if i % 2 == 0:
                    data = data + line

        with open(file, 'w') as outfile:
            outfile.write(data)

    def save_to_csv(self, dataframe, filename):
        # save the dataframe to a csv file
        dataframe.to_csv(filename, sep=',', index=False)

    # Checking if time is in the trading time, i.e. this is a full trading day
    def is_trading_time(self, time):
        startTradingTime = datetime.datetime.strptime('09:30:00', '%H:%M:%S')
        endTradingTime = datetime.datetime.strptime('15:00:00', '%H:%M:%S')
        curTime = datetime.datetime.strptime(time, '%H:%M:%S')
        if curTime >= startTradingTime and curTime <= endTradingTime:
            return True
        pass

    def check_if_this_is_a_full_trading_day(self, day):
        for time in day.Time:
            if self.is_trading_time(time):
                return True
        pass

    def load_data_frame_from_file_with_split_to_five_days_before(self, file_name):
        df = pd.read_csv(file_name, header=0)
        split_date = list(df.groupby("Date").groups.keys())[-6]

        full_trading_days_passed = 0
        total_trading_days_passed = 0
        for i, x in df[::-1].groupby('Date', sort=False):
            total_trading_days_passed += 1
            if self.check_if_this_is_a_full_trading_day(x):
                full_trading_days_passed+=1
            if full_trading_days_passed >= self.trading_days_in_deep:
                break

        #for a in reversed(groupedByDay['Date']):
        #    print(a)

        #for a in groupedByDay['Date']:
        #    print(a)

        #for date in groupedByDay:
        #    print(date)
        #    print(groupedByDay.loc[date])

        #for name, group in df.groupby("Date"):
        #    print(name)
        #    print(group)
        #    print('\n')

        # All records before 5 days
        a = df[df.Date <= self.date_before_five_days ]
        # Last five days
        b = df[df.Date > self.date_before_five_days ]
        return a, b

    def appendDataFrame(self, df1,df2):
        df = df1 + df2
        return df



csv_combiner = CSV_Combiner()
