using HtmlAgilityPack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace STMWPF
{
    /*<table>
        <tr>
            <td width="30%" class="image">
            </td>
            <td width="70%" class="rightPart">
                <tr height="20%" class="itemHeader">
                    <td width="80%" class="name">
                    </td>
                    <td width="20%" class="discount">
                    10
                    </td>
                </tr>
                <tr height="20%" class="otherStuff">
                </tr>
            </td>
        </tr>
    </table>*/
    class DocumentWriter
    {
        HtmlDocument _doc;
        public DocumentWriter()
        {
            _doc = new HtmlDocument();
            var html = HtmlNode.CreateNode("<html><head></head><body></body></html>");
            _doc.DocumentNode.AppendChild(html);
            // select the <head>
            var head = _doc.DocumentNode.SelectSingleNode("/html/head");
            // create a <title> element
            var title = HtmlNode.CreateNode("<title>Hello world</title>");
            // append <title> to <head>
            head.AppendChild(title);
            // returns Hello world!
            var inner = title.InnerHtml;
            // returns <title>Hello world!</title>
            var outer = title.OuterHtml;
            //html.AppendChild(head);
        }

        public void Write(SteamDiscount discount)
        {
            var body = _doc.DocumentNode.SelectSingleNode("/html/body");

            var table = HtmlNode.CreateNode("<table class=\"tableItem\" width=\"100%\"></table>");

            var firstTr = HtmlNode.CreateNode("<tr class=\"item\"></tr>");
            var imageTd = HtmlNode.CreateNode("<td class=\"image\" width=\"30%\">" + "<a href= \"" + discount.url + "\"><img src=" + discount.imageUrl + "></a>" + "</td>");
            
            var rightTd = HtmlNode.CreateNode("<td class=\"rightTD\" width=\"70%\"></td>");
            
            // Right TD
            var rightTrTop = HtmlNode.CreateNode("<tr class=\"rightTop\"></tr>");
            var nameTd = HtmlNode.CreateNode("<td class=\"name\" width=\"70%\">" + discount.name + "</td>");
            var discTd = HtmlNode.CreateNode("<td class=\"disc\" width=\"30%\">" + discount.currentCost + "</td>");
            rightTrTop.AppendChild(nameTd);
            rightTrTop.AppendChild(discTd);
            var rightTrBot = HtmlNode.CreateNode("<tr class=\"rightBot\"></tr>");
            var stuffTd = HtmlNode.CreateNode("<td class=\"stuff\" width=\"30%\">" + "STUFF" + "</td>");
            rightTrBot.AppendChild(stuffTd);
            rightTd.AppendChild(rightTrTop);
            rightTd.AppendChild(rightTrBot);
            firstTr.AppendChild(imageTd);
            firstTr.AppendChild(rightTd);
            table.AppendChild(firstTr);
            //html.AppendChild(HtmlNode.CreateNode("<tr class=\"item\"></tr>"));
            body.AppendChild(table);
        }

        public void SaveToDisk(string path = "Page.html")
        {
            _doc.Save("Page.html");
        }
    }
}
