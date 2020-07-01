using HtmlAgilityPack;
using System;
using System.Net;
using System.Text;
using System.Linq;
using System.Collections.Generic;

namespace STMWPF
{
    public class SteamDiscount
    {
        public SteamDiscount() { }
        public string discount { get; set; }
        public string name { get; set; }
        public string url { get; set; }
        public int currentCost { get; set; }
        public int originalCost { get; set; }
        public int countDiscount { get; set; }
        public string review { get; set; }
        public string gotCards { get; set; }
        public string release { get; set; }
        public string imageUrl { get; set; }
    }

    class WBPRSR
    {
        private WebClient _wClient;
        List<SteamDiscount> _items = new List<SteamDiscount>();
        public List<SteamDiscount> Items { get => _items; }

        public WBPRSR()
        {
            _wClient = new WebClient();
            _wClient.Encoding = Encoding.UTF8;
            HtmlDocument htmlDoc = new HtmlDocument();
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Ssl3 | SecurityProtocolType.Tls | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12;
            //string basePath = "http://store.steampowered.com/search/?filter=weeklongdeals&sort_by=Price_ASC&page=";
            //string basePath = "https://store.steampowered.com/search/?sort_by=Price_ASC&sort_order=ASC&special_categories=&specials=1&page=";
            string basePath = "https://store.steampowered.com/search/?specials=1?page=";
            string path = basePath + "1";
            string xpathToCountPages = "//*[@id=\"search_result_container\"]/div[3]/div[2]/a[3]";
            ////*                            [@id="search_result_container"]/div[3]/div[2]/a[3]
            htmlDoc.LoadHtml(_wClient.DownloadString(new Uri(path)));
            HtmlNodeCollection nodes = htmlDoc.DocumentNode.SelectNodes(xpathToCountPages);
            int pagesCount = 5;
            if (nodes != null)
            {
                pagesCount = Convert.ToInt32( nodes.First().InnerHtml );
                if (pagesCount > 15) pagesCount = 15;
                //pagesCount = 5;
                _items = new List<SteamDiscount>();
                for (int i = 1; i <= pagesCount; i++)
                {
                    path = basePath + i.ToString();
                    htmlDoc.LoadHtml(_wClient.DownloadString(new Uri(path)));
                    GetListItems(htmlDoc);
                    Console.Write("Элементов добавлено " + Items.Count);
                }
                _items = _items.OrderByDescending(o => o.discount).ToList();
            }
        }


        void GetListItems(HtmlAgilityPack.HtmlDocument html)
        {
            //Путь к списку 
            HtmlNodeCollection allGames = html.DocumentNode.SelectNodes("//*[@id=\"search_result_container\"]/div[2]");

            //Путь к конкретному элементу:
            //*[@id="search_result_container"]/div[2]/a[2]

            int elements_count = 0;
            if (allGames != null)
            {
                elements_count = allGames.First().ChildNodes.Where(x => (x.Name == "a")).Count();
            }

            //*[@id="search_result_container"]/div[2]/a[1]/div[2]/div[1]/span                   NAME
            //*[@id="search_result_container"]/div[2]/a[1]/div[2]/div[2]                        RELEASE
            //*[@id="search_result_container"]/div[2]/a[4]/div[2]/div[3]/span                   REVIEW
            //*[@id="search_result_container"]/div[2]/a[1]/div[2]/div[4]/div[1]/span            DISCOUNT
            //*[@id="search_result_container"]/div[2]/a[1]/div[2]/div[4]/div[2]/span/strike     PREV PRICE
            //*[@id="search_result_container"]/div[2]/a[1]/div[2]/div[4]/div[2]/text()          CURRENT PRICE     
            //*[@id="search_result_container"]/div[2]/a[1]                                      URL       

            SteamDiscount array_item;
            for (int i = 1; i <= elements_count; i++)
            {
                array_item = new SteamDiscount();
                HtmlNode name = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[1]/span");
                HtmlNode release = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[2]");
                //HtmlNode review = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[3]/span");
                //HtmlNode review = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[3]");
                HtmlNode discount = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[4]/div[1]/span");
                HtmlNode strike = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[4]/div[2]/span");
                HtmlNode current = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]/div[2]/div[4]/div[2]");
                HtmlNode steam_url = html.DocumentNode.SelectSingleNode("//*[@id=\"search_result_container\"]/div[2]/a[" + i.ToString() + "]");

                try
                {
                    array_item.name = (name.InnerText != null) ? name.InnerText : "";
                    Console.Write(array_item.name);

                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {
                    array_item.release = (!String.IsNullOrEmpty(release.InnerText)) ? release.InnerText : "";
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {
                    array_item.discount = (!String.IsNullOrEmpty(discount.InnerText)) ? discount.InnerText : "0";
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {
                    array_item.originalCost = (Int32.Parse(strike.InnerText.Split(' ')[0]) != null) ? Int32.Parse(strike.InnerText.Split(' ')[0]) : 0;
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {
                    array_item.currentCost = Int32.Parse(current.InnerHtml.Split(new string[] { "<br>" }, StringSplitOptions.None)[1].Replace("\t", "").Split(' ')[0]);
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {

                    //var temp1 = review.InnerHtml;
                    //var temp2 = review.HasChildNodes;
                    //var temp3 = review.FirstChild;
                    //var temp4 = review.ChildNodes;
                    //var temp5 = review.Attributes;
                    //var temp6 = review.HasClosingAttributes;
                    //var temp7 = review.ChildAttributes("");
                    //# search_result_container > div:nth-child(2) > a.search_result_row.ds_collapse_flag.ds_owned.es_ea_checked.app_impression_tracked.es_highlight_checked.es_highlighted.es_highlighted_owned > div.responsive_search_name_combined > div.col.search_reviewscore.responsive_secondrow
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {
                    array_item.countDiscount = array_item.originalCost - array_item.currentCost;
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                try
                {
                    array_item.url = steam_url.Attributes[0].Value;
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                Items.Add(array_item);
                try
                {
                    array_item.imageUrl = LoadAdditionData(array_item.url); ;
                }
                catch
                {
                    Console.Write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!");
                }
                Items.Add(array_item);
            }

            return;
        }

        public string LoadAdditionData(string url)
        {
            //need to load page to get image and score
            //image path: //*[@id="game_highlights"]/div[1]/div/div[1]/img
            //score path: //*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[1]
            WebClient wClient = new WebClient();
            HtmlDocument htmlDoc = new HtmlDocument();
            htmlDoc.LoadHtml(wClient.DownloadString(new Uri(url)));
            HtmlNodeCollection score = htmlDoc.DocumentNode.SelectNodes("//*[@id=\"game_highlights\"]/div[1]/div/div[3]/div/div[2]/div[2]/span[1]");
            HtmlNodeCollection image = htmlDoc.DocumentNode.SelectNodes("//*[@id=\"game_highlights\"]/div[1]/div/div[1]/img");
            if (image != null) return image[0].Attributes[1].Value;
            return null;
        }
    }
}
