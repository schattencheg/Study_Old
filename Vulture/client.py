import math, time, os, sys
import pandas, numpy, datetime, random
import socket, json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
import zope.event

class Value():
    def __init__(self, min, max, cur):
        self.min = min
        self.max = max
        self.cur = cur

class Requester():
    def __init__(self, request_string = b'VSKD_STRING_LEN=00000022{"Sys":"Kipelovo_VSKD","Pack":4}\r\n', address = "80.80.96.154", port = 5000):
        self.request = request_string
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((address, port))
        except WindowsError:
            print("Cannot connect to the server!")
            zope.event.notify(sys.exc_info()[0])
        self.df = pandas.DataFrame(columns = ['Date'], index=['Date'])
        self.dataframes = {}
        self.delay = 1
        self.data_path = "Data"

    def SendRequest(self, request):
        totalsent = 0
        request_length = len(request)
        while totalsent < request_length:
            sent = self.socket.send(request[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        data = self.socket.recv(1024)
        return data.decode("utf-8")[24:-3]

    def EvaluateRequest(self):
        cur_time = datetime.datetime.now()
        rcvmsg = self.SendRequest(self.request)
        js = json.loads(rcvmsg)

        dmp = json.dumps(js, indent = 4)
        e = {"Date":cur_time}
        for system_key in js.keys():
            system_element = js[system_key] 
            #print(system_key,":",system_element,type(js[system_key]))
            if "mod " in system_key:
                for module_key in system_element:
                    cur_module_element = system_element[module_key] 
                    #print(module_key,":",cur_module_element)
                    if "obj " in module_key:
                        for object_key in cur_module_element:
                            cur_object_element = cur_module_element[object_key] 
                            if "Val" in object_key:
                                val = Value(cur_object_element['Min'],cur_object_element["Max"],cur_object_element["Cur"])
                                sys_name = system_key[4:]
                                obj_name = module_key[4:]
                                _min = sys_name + "_" + obj_name + "_" + "Min"
                                _max = sys_name + "_" + obj_name + "_" + "Max"
                                _cur = sys_name + "_" + obj_name + "_" + "Cur"
                                e[_min] = val.min
                                e[_max] = val.max
                                e[_cur] = val.cur
                                dataframe_name = sys_name + "_" + obj_name
                                if not dataframe_name in self.dataframes.keys():
                                    self.dataframes[dataframe_name] = pandas.DataFrame(columns=["Date","Cur","Min","Max"], index = ["Date"])
                                self.dataframes[dataframe_name] = self.dataframes[dataframe_name].append({"Date":cur_time, "Cur":val.cur, "Min":val.min, "Max":val.max}, ignore_index=True)
                            else:
                                #print(object_key,":",cur_object_element)
                                pass
        self.df = self.df.append(e, ignore_index=True)

    def GetSensors(self):
        return list(self.dataframes.keys())

    def GetSensorData(self, sensor):
        return self.dataframes[sensor]
    
    def SaveData(self):
        for key in self.dataframes.keys():
            if not os.path.exists(self.data_path):
                os.makedirs(self.data_path)
            filename = self.data_path + "\\" + key + ".csv"
            #print("Saving '{}' to '{}'.".format(key,filename))
            try:
                self.dataframes[key].to_csv(filename)
            except:
                print("Can't write to file {}.".format(filename))

    def Run(self, delay = 1):
        self.delay = delay
        while True:
            self.EvaluateRequest()
            #if self.df.size % 10 == 0:
            #    zope.event.notify(self.df.size)
            zope.event.notify(self.df.size)
            time.sleep(self.delay)            

    def Plot(self):
        pass

class Indicator():
    def __init__(self, width, height, min, max, normal_low, normal_high):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.surface = pygame.Surface(self.size)
        self.min = min
        self.normal_min = normal_low
        self.max = max
        self.normal_max = normal_high

        self.color = (0,255,0)
        self.Requester = Requester()
        pygame.draw.rect(self.surface, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), pygame.Rect(1, 1, self.width - 1, self.height - 1))

    def Update(self, value, min, max):
        self.value = value

    def Surface(self):
        self.surface.fill(255,255,255)
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(1, 1, self.width - 1, self.height - 1), width = 3)
        if self.value >= self.normal_max:
            self.color = (255,0,0)
            y = self.height - 1
        elif self.value <= self.normal_min:
            self.color = (255,0,0)
            y = 1
        else:
            self.color = (0,255,0)
            y = 1 + (self.value - self.min)/(self.max - self.min) * (self.height - 2)
        pygame.draw.rect(self.surface, self.color, pygame.Rect(1, 1, self.width - 1, y))
        return self.surface

class Display():
    def __init__(self, count = 1):
        pygame.init()
        width = 500
        height = 500
        self.display = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        self.loop = True
        self.instances = []
        self.rects = []
        self.sector_count = math.sqrt(count)

        for i in range(count):
            instance = Indicator(width = width, height = height, min = -200, max = 200, normal_low = 10, normal_high=40)
            self.instances.append(instance)
            x = i % sector_count
            y = i // sector_count
            self.sector_width = round(min(width,height) / sector_count)
            self.rects.append((x * self.sector_width, y * self.sector_width, (x + 1) * self.sector_width, (y + 1) * self.sector_width))

    def Loop(self):
        while True:
            for i in range(count):
                instance = self.instances[i]
                instance.update()
                image = instance.GetImage()
                gameDisplay.blit(pygame.transform.scale(image,(self.sector_width, self.sector_width)), self.rects[i])

class SensorViewer():
    def __init__(self):
        zope.event.subscribers.append(self.OnEvent)
        self.requester = Requester()
        self.requester.Run(delay = 0)

    def OnEvent(self, event):
        if isinstance(event, numpy.int32):
            self.requester.df.to_csv("data.csv")
            self.requester.SaveData()
            self.DrawSensor()
        else:
            print(event)
            sys.exit()

    def animate(self, i, xs, ys):
        # Read temperature (Celsius) from TMP102
        #temp_c = round(tmp102.read_temp(), 2)

        # Add x and y to lists
        #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        #ys.append(temp_c)

        # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]

        # Draw x and y lists
        self.ax.clear()
        self.ax.plot(xs, ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Title')
        plt.ylabel('Temperature')

    def DrawSensor(self):
        sensors = self.requester.GetSensors()
        if len(sensors) == 0:
            return
        df = self.requester.GetSensorData(sensors[0]).set_index("Date")
        x = df.index.values[1:]
        y_cur = df["Cur"].values[1:]
        y_min = df["Min"].values[1:]
        y_max = df["Max"].values[1:]

        # Create figure for plotting
        fig = plt.figure()
        self.ax = fig.add_subplot(1, 1, 1)
        xs = x
        ys = y_cur

        ani = animation.FuncAnimation(fig, self.animate, fargs=(xs, ys), interval=1000)
        plt.show()
        return

        print("ASD")
        plt.scatter(x, y_min)
        plt.scatter(x, y_max)
        plt.scatter(x, y_cur)
        plt.show()

sensorViewer = Display()
