using PriceConverter.ViewModels;
using System.ComponentModel;
using Xamarin.Forms;

namespace PriceConverter.Views
{
    public partial class ItemDetailPage : ContentPage
    {
        public ItemDetailPage()
        {
            InitializeComponent();
            BindingContext = new ItemDetailViewModel();
        }
    }
}