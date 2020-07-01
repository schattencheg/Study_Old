using QuantConnect.Data.Consolidators;
using QuantConnect.Data.Fundamental;
using QuantConnect.Data.Market;
using QuantConnect.Data.UniverseSelection;
using QuantConnect.Indicators;
using QuantConnect.Orders;
using System;
using System.Collections.Generic;
using System.Linq;

namespace QuantConnect.Algorithm.CSharp
{
    class Streak
    {
        private int currentStreak;
        private int maxStreak;
        public int MaxStreak { get { return maxStreak; } set { maxStreak = value; } }
        public Streak() { currentStreak = 0; MaxStreak = 0; }
        public void streak() { currentStreak++; }
        public void breakStreak() { if (currentStreak > MaxStreak) MaxStreak = currentStreak; currentStreak = 0; }
    }
    class Counter
    {
        int[] positions;

        public Counter(int count)
        {
            positions = new int[count];
        }

        public int Count()
        {
            return positions.Count(x => x != 0);
        }
    }
    class PLRSI : RelativeStrengthIndex
    {
        private decimal low;
        private decimal high;
        private decimal prev;
        private int prevStatus;
        private int Status;
        public decimal Low { get { return low; } set { low = value; } }
        public decimal High { get { return high; } set { high = value; } }
        public void Iterate()
        {
            int result = prevStatus;
            if (prev != -500)
            {
                if ((Current.Value > Low) && (prev <= Low))
                    result = 1;
                else
                    if ((Current.Value < High) && (prev >= High))
                    result = -10;
            }
            prev = Current.Value;
            prevStatus = result < 0 ? 0 : 1;
            Status = result;
        }
        public int status { get { return Status; } }
        public PLRSI(string name, int period, MovingAverageType movingAverageType = MovingAverageType.Wilders) : base(name, period, movingAverageType)
        {
            prev = -500;
            prevStatus = 0;
        }
    }
    class PLMFI : MoneyFlowIndex
    {
        private decimal low;
        private decimal high;
        private decimal prev;
        private int prevStatus;
        private int Status;
        public decimal Low { get { return low; } set { low = value; } }
        public decimal High { get { return high; } set { high = value; } }
        public void Iterate()
        {
            int result = prevStatus;
            if (prev != -500)
            {
                if ((Current.Value > Low) && (prev <= Low))
                    result = 1;
                else
                    if ((Current.Value < High) && (prev >= High))
                    result = -10;
            }
            prev = Current.Value;
            prevStatus = result < 0 ? 0 : 1;
            Status = result;
        }
        public int status { get { return Status; } }
        public PLMFI(string name, int period) : base(name, period)
        {
            prev = -500;
            prevStatus = 0;
        }
    }
    class PLADI : AverageDirectionalIndex
    {
        private decimal low;
        private decimal high;
        private decimal prev;
        private int prevStatus;
        private int Status;
        public decimal Low { get { return low; } set { low = value; } }
        public decimal High { get { return high; } set { high = value; } }
        public void Iterate()
        {
            int result = prevStatus;
            if (prev != -500)
            {
                if ((Current.Value > Low) && (prev <= Low))
                    result = 1;
                else
                    if ((Current.Value < High) && (prev >= High))
                    result = -10;
            }
            prev = Current.Value;
            prevStatus = result < 0 ? 0 : 1;
            Status = result;
        }
        public int status { get { return Status; } }
        public PLADI(string name, int period) : base(name, period)
        {
            prev = -500;
            prevStatus = 0;
        }
    }
    class PLCMO : ChandeMomentumOscillator
    {
        private decimal low;
        private decimal high;
        private decimal prev;
        private int prevStatus;
        private int Status;
        public decimal Low { get { return low; } set { low = value; } }
        public decimal High { get { return high; } set { high = value; } }
        public void Iterate()
        {
            int result = prevStatus;
            if (prev != -500)
            {
                if ((Current.Value > Low) && (prev <= Low))
                    result = 1;
                else
                    if ((Current.Value < High) && (prev >= High))
                    result = -10;
            }
            prev = Current.Value;
            prevStatus = result < 0 ? 0 : 1;
            Status = result;
        }
        public int status { get { return Status; } }
        public PLCMO(string name, int period) : base(name, period)
        {
            prev = -500;
            prevStatus = 0;
        }
    }
    class PLUO : UltimateOscillator
    {
        private decimal low;
        private decimal high;
        private decimal prev;
        private int prevStatus;
        private int Status;
        public decimal Low { get { return low; } set { low = value; } }
        public decimal High { get { return high; } set { high = value; } }
        public void Iterate()
        {
            int result = prevStatus;
            if (prev != -500)
            {
                if ((Current.Value > Low) && (prev <= Low))
                    result = 1;
                else
                    if ((Current.Value < High) && (prev >= High))
                    result = -10;
            }
            prev = Current.Value;
            prevStatus = result < 0 ? 0 : 1;
            Status = result;
        }
        public int status { get { return Status; } }
        public PLUO(string name, int period1, int period2, int period3) : base(name, period1, period2, period3)
        {
            prev = -500;
            prevStatus = 0;
        }
    }
    class IndicatorSet
    {
        Symbol _innerSymbol;
        bool[] _strategySignals;
        QCAlgorithm _parent;
        public PLRSI RSI;
        public PLMFI MFI;
        public PLADI ADI;
        public PLCMO CMO;
        public PLUO UO;

        public IndicatorSet(QCAlgorithm parent, Symbol symbol, bool[] strategySignals)
        {
            _innerSymbol = symbol;
            _strategySignals = strategySignals;
            _parent = parent;
            //                AddIndicators();
        }
        public void AddIndicators()
        {
            var consolidator = new TradeBarConsolidator(TimeSpan.FromMinutes(1));

            if (_strategySignals[0])
            {
                RSI = new PLRSI(_innerSymbol.Value.ToString(), 21, MovingAverageType.Simple)
                {
                    Low = 40,
                    High = 80
                };
                _parent.RegisterIndicator(_innerSymbol, RSI, consolidator);
            }
            if (_strategySignals[1])
            {
                MFI = new PLMFI(_innerSymbol.Value.ToString(), 40)
                {
                    Low = 40,
                    High = 80
                };
                _parent.RegisterIndicator(_innerSymbol, MFI, consolidator);
            }
            if (_strategySignals[2])
            {
                ADI = new PLADI(_innerSymbol.Value.ToString(), 14)
                {
                    Low = -50,
                    High = 100
                };
                _parent.RegisterIndicator(_innerSymbol, ADI, consolidator);
            }
            if (_strategySignals[3])
            {
                CMO = new PLCMO(_innerSymbol.Value.ToString(), 14)
                {
                    Low = 20,
                    High = 70
                };
                _parent.RegisterIndicator(_innerSymbol, CMO, consolidator);
            }
            if (_strategySignals[4])
            {
                UO = new PLUO(_innerSymbol.Value.ToString(), 7, 14, 28)
                {
                    Low = 40,
                    High = 80
                };
                _parent.RegisterIndicator(_innerSymbol, UO, consolidator);
            }
        }
        public void Plot()
        {
            if (_strategySignals[0])
                _parent.PlotIndicator("RSI_" + _innerSymbol.Value.ToString(), RSI);
            if (_strategySignals[1])
                _parent.PlotIndicator("MFI_" + _innerSymbol.Value.ToString(), MFI);
            if (_strategySignals[2])
                _parent.PlotIndicator("ADI_" + _innerSymbol.Value.ToString(), ADI);
            if (_strategySignals[3])
                _parent.PlotIndicator("CMO_" + _innerSymbol.Value.ToString(), CMO);
            if (_strategySignals[4])
                _parent.PlotIndicator("UO_" + _innerSymbol.Value.ToString(), UO);
        }
        public int[] Status()
        {
            int[] result = new int[5];
            if (_strategySignals[0]) { RSI.Iterate(); result[0] = RSI.status;}
            if (_strategySignals[1]) { MFI.Iterate(); result[1] = MFI.status;}
            if (_strategySignals[2]) { ADI.Iterate(); result[2] = ADI.status;}
            if (_strategySignals[3]) { CMO.Iterate(); result[3] = CMO.status;}
            if (_strategySignals[4]) { UO.Iterate(); result[4] = UO.status; }
            return result;
        }
        public override string ToString()
        {
            return string.Join(" ", _strategySignals[0]);
        }
    }
    public class _PL_Universe_Selection : QCAlgorithm
    {
        Resolution globalResolution = Resolution.Daily;
        const int StrategyInstrumentsCount = 3;
        const int StrategyMinimalSignalsCount = 2;
        readonly bool[] strategySignals = { /*RSI*/true, /*MFI*/false, /*ADI*/false, /*CMO*/false, /*UO*/false };

        Dictionary<Symbol, IndicatorSet> allSymbols = new Dictionary<Symbol, IndicatorSet>();
        Dictionary<Symbol, Streak> Streaks = new Dictionary<Symbol, Streak>();
        Dictionary<Symbol, int> needToPurchase = new Dictionary<Symbol, int>(); //-1 sell, 0 nothing, +1 buy

        SecurityChanges _universeChanges = SecurityChanges.None;
        private bool _needToRebalance = true;
        private bool DoDebug = false;
        private int monthlyCount = 12;

        public override void Initialize()
        {
            UniverseSettings.Resolution = globalResolution;
            SetStartDate(1998, 1, 1);  //Set Start Date
            SetEndDate(2018, 9, 1);     //Set End Date
            SetCash(1000000);           //Set Strategy Cash
            var spy = AddEquity("SPY", Resolution.Daily);
            Schedule.On(DateRules.MonthStart("SPY"), TimeRules.At(0, 0), Rebalance);
            Rebalance();
        }
        private void Rebalance()
        {
            monthlyCount++;
            if (monthlyCount >= 12)
            {
                if (DoDebug) Debug("Start to reinvesting portfolio...");
                _needToRebalance = true;
                AddUniverse(CoarseSelectionFunction, FineSelectionFunction);
                if (DoDebug) Debug("Done!");
                monthlyCount = 0;
            }
        }
        public IEnumerable<Symbol> CoarseSelectionFunction(IEnumerable<CoarseFundamental> coarse)
        {
            if (!_needToRebalance)
                return new List<Symbol>(UniverseManager.ActiveSecurities.Keys);
            var sortedByDollarVolume = from x in coarse
                                       where x.HasFundamentalData && x.Volume > 0 && x.Price > 0
                                       orderby x.DollarVolume descending
                                       select x;
            var top = sortedByDollarVolume.Take(StrategyInstrumentsCount).ToList();
            return top.Select(x => x.Symbol);
        }
        public IEnumerable<Symbol> FineSelectionFunction(IEnumerable<FineFundamental> fine)
        {
            _needToRebalance = false;
            return fine.Select(x => x.Symbol);
        }
        public void OnData(TradeBars data)
        {
            int ntpCount = 0; //Need to purchase count
            foreach (var tmp in data)
            {
                string name = tmp.Key.ToString();
                Symbol symbol = tmp.Key;

                if (symbol.Value.ToString() == "SPY") continue;
                decimal price = tmp.Value.Close;
                int[] status = allSymbols[symbol].Status();

                if (DoDebug) { IndicatorSet iSet = allSymbols[symbol]; iSet.Plot(); }
                if (symbol.Value.ToString() == "AAPL") { allSymbols[symbol].Plot(); }

                int count = 0;
                for (int i = 0; i < strategySignals.Length; i++)
                    if (strategySignals[i]) { count += status[i]; Log(status[i]); } //If indicator applied to strategy

                //Check if count exceed minimal signals count
                int ntp = 0;
                if ((count >= StrategyMinimalSignalsCount) && !Portfolio[symbol].Invested) { ntp = 1; ntpCount++; }
                else if ((count < 0) && Portfolio[symbol].Invested) { ntp = -1; }
                needToPurchase[symbol] = ntp;
            }

            int investedCount = 0;
            if (Portfolio.HoldStock)
            {
                foreach (var val in Portfolio)
                {
                    Symbol nm = val.Key;
                    if ((Portfolio[nm].Invested) && (needToPurchase[nm] == 0)) investedCount++;
                    if ((Portfolio[nm].Invested) && (needToPurchase[nm] < 0))
                    {
                        investedCount--;
                        Liquidate(nm, allSymbols[nm].ToString());
                    }
                }
            }
            int totalCount = investedCount + ntpCount;

            foreach (var tmp in needToPurchase)
            {
                if (tmp.Value > 0)
                {
                    SetHoldings(tmp.Key, 1.0 / (totalCount));
                }
            }
            needToPurchase.Clear();
        }
        //public decimal GetQuantity(decimal price)
        //{
        //    decimal result = 0;
        //    result = Portfolio.Cash / StrategyInstrumentsCount / price;
        //    return result;
        //}
        public override void OnOrderEvent(OrderEvent orderEvent)
        {
            var order = Transactions.GetOrderById(orderEvent.OrderId);
            if (orderEvent.Status == OrderStatus.Filled)
            {
                if (DoDebug) Log("Order " + order.Symbol.Value.ToString() + " filled");
                if (order.Direction == OrderDirection.Sell)
                {
                    Symbol symbol = order.Symbol;
                    decimal openPrice = order.OrderSubmissionData.BidPrice;
                    decimal closePrice = order.Price;
                    decimal profit = closePrice - openPrice;
                    if (profit >= 0)
                        Streaks[symbol].streak();
                    else
                        Streaks[symbol].breakStreak();
                }
            }
            else if (orderEvent.Status == OrderStatus.Submitted)
            {

            }
            else if (orderEvent.Status == OrderStatus.Invalid)
            {
                if (DoDebug) Log("Order " + order.Symbol.Value.ToString() + " INVALID (wanted " + Portfolio.GetBuyingPower(orderEvent.Symbol) + " have " + orderEvent.FillQuantity + ")");
            }
            else if (DoDebug) Log("Order " + order.Symbol.Value.ToString() + " " + orderEvent.Status);
        }
        public override void OnEndOfAlgorithm()
        {
            base.OnEndOfAlgorithm();
            foreach (var tmp in Streaks)
            {
                Log("Streak for " + tmp.Key.Value.ToString() + " " + tmp.Value.MaxStreak);
            }
        }
        public override void OnSecuritiesChanged(SecurityChanges changes)
        {
            foreach (var tmp in UniverseManager.ActiveSecurities)
            {
                Symbol _symbol = tmp.Key;
                if (!allSymbols.ContainsKey(_symbol))
                {
                    IndicatorSet iSet = new IndicatorSet(this, _symbol, strategySignals);
                    iSet.AddIndicators();
                    allSymbols.Add(_symbol, iSet);
                    Streaks.Add(_symbol, new Streak());
                    if (DoDebug) Debug("Added instrument: " + _symbol.Value.ToString());
                }
            }
            _universeChanges = changes;
            foreach (var tmp in changes.RemovedSecurities)
            {
                Liquidate(tmp.Symbol, "Removed");
            }
        }
    }
}
