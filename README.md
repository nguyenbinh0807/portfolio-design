# markowitzvn
*markowitzvn* is a program for financial **portfolio management, analysis and optimisation**.

## Table of contents
 - [Motivation](#Motivation)
 - [Automatically generating an instance of](#DataLoad)
 - [LinePlot](#LinePlot)
- [Portfolio Management](#Portfolio-Management)
 - [Installation](#Installation)
 - [Contact Information](#Contact-Information)
## Motivation
*markowitzvn* có thể tạo một đối tượng giữ giá cổ phiếu của danh mục đầu tư tài chính bạn mong muốn, phân tích nó và có thể tạo các biểu đồ gồm các loại *Returns*, *Moving Averages*, *Line Plot*. Nó cũng cho phép tối ưu hóa dựa trên *Efficient Frontier* hoặc danh mục đầu tư tài chính chạy *Monte Carlo* trong một vài dòng mã. Một số kết quả được hiển thị ở đây.
Dựa trên lý thuyết tối đa hóa danh mục đầu tư của markowitz và những yêu cầu để phù hợp với thị trường Việt Nam nên tôi đã đưa mô hình về với Việt Nam giúp cho nhà đầu tư trong việc phân tích và phân bổ danh mục tối đa lợi nhuận và giảm thiểu rủi ro.

### Automatically generating an instance of `DataLoad`
`DataLoad()` là một hàm đầu vào là *symbols* *start*  *end* sẽ trả về kết quả một dataframe giá cổ phiếu trong khoảng thời gian đầu vào .
```
import markowitzvn.data as dt
symbols_list=['CTG', 'MBB', 'FMC', 'CMG', 'FPT']
start_date = '2019-11-15'
end_date = '2022-11-15'
loader=dt.DataLoad(symbols=symbols_list, start=start_date, end=end_date)
```
`loader` chứa giá cổ phiếu trong danh mục đầu tư của bạn, sau đó...
```
price_stock=loader.download()
>>price_stock
```
Results
```
              CTG      MBB      FMC      CMG      FPT
TradingDate                                             
2019-11-18   15956.0  12130.0  21608.0  24944.0  33409.0
2019-11-19   16031.0  12211.0  21688.0  24944.0  33874.0
2019-11-20   15882.0  12130.0  21688.0  24588.0  33003.0
2019-11-21   15882.0  12023.0  21688.0  24717.0  32538.0
2019-11-22   15733.0  11996.0  21489.0  24588.0  32538.0
...              ...      ...      ...      ...      ...
2022-11-09   24450.0  16950.0  35000.0  35400.0  74000.0
2022-11-10   22750.0  15800.0  34350.0  33950.0  73000.0
2022-11-11   23600.0  16000.0  34700.0  35000.0  72800.0
2022-11-14   23900.0  15200.0  33000.0  35000.0  70800.0
2022-11-15   23400.0  14150.0  30700.0  32550.0  65900.0
```
Nếu đầu vào của bạn là một cổ phiếu
```
import markowitzvn.data as dt
symbols_list='FPT'

start_date = '2019-11-15'
end_date = '2022-11-15'
loader=dt.DataLoad(symbols=symbols_list, start=start_date, end=end_date)
price_stock=loader.download()
>>price_stock
```
Results

```
                Open     High      Low    Close   Volume
TradingDate                                             
2019-11-18   33932.0  34165.0  33177.0  33409.0  2794920
2019-11-19   33409.0  33874.0  33409.0  33874.0  1059770
2019-11-20   33816.0  33816.0  32886.0  33003.0  2291760
2019-11-21   33003.0  33177.0  32480.0  32538.0  3303950
2019-11-22   32712.0  33177.0  32247.0  32538.0  1625820
...              ...      ...      ...      ...      ...
2022-11-09   73300.0  74300.0  73300.0  74000.0   699349
2022-11-10   73500.0  73700.0  69100.0  73000.0  1598605
2022-11-11   73100.0  73600.0  72000.0  72800.0  1004524
2022-11-14   72000.0  72400.0  70000.0  70800.0  1642109
2022-11-15   70000.0  70000.0  65900.0  65900.0  3123365
```
### Line plot
trực quan giá cổ phiếu bằng biểu đồ đường.
Nếu bạn muốn so sánh giá cổ phiếu với nhau có một tham số *permanent=True* nó sẽ cố định một điểm bắt đầu là 100.
```
loader.lineplot()
  """this is a vizual pirce close

        Args:
            permanent (bool, optional): if True permanent start else . Defaults to False.
        """
```
yields
<p align="center">
  <img src="images/Screenshot 2022-12-15 140013.png" width="90%">
</p>

### Portfolio properties
In ra các thuộc tính danh mục đầu tư, yêu cầu đầu vào phải năm cổ phiếu mới thực hiện được hàm này 
```
 """this is a properties 

        Args:
            num_portfolios (int, optional): number portfolios. Defaults to 6000.
            risk_free_rate (float, optional): _description_. Defaults to 0.07.
            vizual (bool, optional): if True vizual camp. Defaults to False.

        Returns:
            _type_: weights, returns, vol
        """
      
loader.properties(vizual=True)
```
results

```
Maximum Sharpe Ratio Portfolio Allocation

Annualised Return: 0.15
Annualised Volatility: 0.29


              CTG    MBB   FMC    CMG     FPT
allocation  28.99   0.01   21.0   20.0   30.0
--------------------------------------------------------------------------------
Minimum Volatility Portfolio Allocation

Annualised Return: 0.13
Annualised Volatility: 0.28


             CTG    MBB       FMC      CMG       FPT
allocation  9.35    19.65    21.0     20.0      30.0
```
Notes:
- Maximum Sharpe Ratio Portfolio Allocation: Tối đa lợi nhuận.
- Minimum Volatility Portfolio Allocation: Giảm thiểu rủi ro.
- Annualised Return: Lợi nhuận.
- Annualised Volatility: Biến động
- allocation: tỷ trọng các cổ phiếu

<p align="center">
  <img src="images\profolios.png" width="90%">
</p>

## Returns
Daily returns of stocks are often computed in different ways. *markowitzvn* provides three different ways of computing the daily returns in `markowitzvn.returns`:
1. The cumulative return: <img src="https://raw.githubusercontent.com/fmilthaler/finquant/master/tex/738645698dc3073b4bb52a0c078ae829.svg?invert_in_darkmode&sanitize=true" align=middle width=194.52263655pt height=46.976899200000005pt/>
2. Percentage change of daily returns: <img src="https://raw.githubusercontent.com/fmilthaler/finquant/master/tex/27215e5f36fd0308b51ab510444edf0d.svg?invert_in_darkmode&sanitize=true" align=middle width=126.07712039999997pt height=48.84266309999997pt/>
3. Log Return: <img src="https://raw.githubusercontent.com/fmilthaler/finquant/master/tex/ef37c00ad58fe657a64041c3093e0640.svg?invert_in_darkmode&sanitize=true" align=middle width=208.3327686pt height=57.53473439999999pt/>

## Installation
As it is common for open-source projects, there are several ways to get hold of the code. Choose whichever suits you and your purposes best.

### Dependencies
*markowitzvn* depends on the following Python packages:
 - numpy>=1.20.2
 - pandas>=0.19.2
 - plotly>=4.2.1
 - scipy>=1.2.0
 - vnstock
 - requests

### From PyPI
*markowitzvn* can be obtained from PyPI

```pip install markowitzvn```

# III. 🙋‍♂️ Contact Information
Hiện tại tôi đang học ngành kinh tế năm 3 tại đại học mở và tự học thêm kỹ năng lập trình để có thể áp dụng vào lĩnh vực kinh tế. Đây là thư viện đầu tiên tôi viết và nếu muốn ủng hộ các thư viện trong việc phân tích thị trường chứng khoán thì qua ngân hàng agribank. Cảm ơn mọi người rất nhiều.

<p align="center">
  <img src="images\37d24aebd151080f5140.jpg" width="60%">
</p>

Nếu ai muốn cùng tôi phát triển các dự án sau này và cùng nhau học hỏi kinh nghiệm. Mọi người có thể liên hệ tôi qua FaceBook. Cảm ơn mọi người
<div id="badges" align="center">
  <a href="https://www.facebook.com/binh.nguyenthe.5815255/">
    <img src="https://img.shields.io/badge/Messenger-00B2FF?style=for-the-badge&logo=messenger&logoColor=white" alt="Messenger Badge"/>
  </a>
</div>
