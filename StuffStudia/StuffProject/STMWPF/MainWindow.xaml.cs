using System.Windows;
using System.Windows.Controls;
using System.Linq;

namespace STMWPF
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        WBPRSR STMLSTNR;
        DocumentWriter _documentWriter;

        public MainWindow()
        {
            InitializeComponent();
            ButtonLoad.Click += LoadButtonClick;
        }

        private void LoadButtonClick(object sender, RoutedEventArgs e)
        {
            STMLSTNR = new WBPRSR();

            _documentWriter = new DocumentWriter();


            foreach (var item in STMLSTNR.Items)
            {
                _documentWriter.Write(item);
                ListBox1.Items.Add(item.name + "   " + item.discount);
                ListBox1.Items.Add("    " + item.currentCost + " <----- " + item.originalCost);
                ListBox1.Items.Add("    " + item.review);
                ListBox1.Items.Add("    " + item.url);
                
                if (item.gotCards != "")
                    ListBox1.Items.Add("    " + item.gotCards);
            }
            _documentWriter.SaveToDisk();
        }
        private void ListBox1SelectionChanged(object sender, RoutedEventArgs e)
        {
            string url = (sender as ListBox).SelectedItem.ToString().Trim();

            string path = "";
            var splittedPath = path.Split('.').Take(path.Split('.').Length - 1).Aggregate((i, j) => i + '.' + j);
            //var newPath = splittedPath.Take()


            if (url.StartsWith("https"))
            {
                STMLSTNR.LoadAdditionData(url);
                //System.Diagnostics.Process.Start(url);
            }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            STM2 stm2 = new STM2();
            var tmpStr = stm2.SendRequest();
            ListBox1.Items.Add(tmpStr);
        }
    }
}
