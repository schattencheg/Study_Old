using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SteamWebAPI2;
using SteamWebAPI2.Interfaces;

namespace STMWPF
{
    class STM2
    {
        SteamUser steamInterface = new SteamUser("<8612C9DA544ADEB74C4E75FBDCC2E6E0>");
        public STM2()
        {

        }

        public string SendRequest()
        {
            // this will map to ISteamUser/GetPlayerSummaries method in the Steam Web API
            // see PlayerSummaryResultContainer.cs for response documentation
            var playerSummaryResponse = /*await */steamInterface.GetFriendsListAsync();//GetPlayerSummaryAsync("schattencheg");
            var playerSummaryData = playerSummaryResponse.Data;
            var playerSummaryLastModified = playerSummaryResponse.LastModified;

            // this will map to ISteamUser/GetFriendsListAsync method in the Steam Web API
            // see FriendListResultContainer.cs for response documentation
            var friendsListResponse = await steamInterface.GetFriendsListAsync("schattencheg");
            var friendsList = friendsListResponse.Data;
            return "";
        }
    }
}
