
!pip install pandas
!pip install yfinance
!pip install matplotlib
!pip install arch
!pip install scipy
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm
from arch import arch_model
import scipy.stats as stats
from scipy.stats import anderson
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import datetime as dt
from statsmodels.graphics.tsaplots import plot_acf

cotacao = yf.Ticker('NVDA')
cotacao = cotacao.history(start="2019-01-01",end="2025-01-01")
dados = np.log(cotacao["Close"]).diff().dropna()

plt.figure(figsize=(10, 6))
plt.plot(cotacao.index, cotacao["Close"], label="IBOV",alpha=1)
plt.xlabel("Período")
plt.ylabel("Valor em U$")
plt.title("Cotação Histórica da NVIDIA")
plt.grid(True)

plt.show()

dados.std()

dados.mean()

media = dados.mean()
desvio = dados.std()
plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7,density=True)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, media, desvio)
plt.xlabel("Desvios Padrões dos Retornos",fontsize=20)
plt.ylabel("Frequencia",fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.style.use('Solarize_Light2')
plt.plot(x, p, 'k', linewidth=2,color="black")

normal = anderson(dados)
print(normal)

intervalo_confianca = 0.95
montante = 100000

z = stats.norm.ppf(intervalo_confianca)

t = stats.t.ppf(1 - intervalo_confianca, len(dados)-1)

VaR = (np.percentile(dados,100*(1 - intervalo_confianca))*montante)

print(f"O VaR Historico é:{VaR}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR/montante),color="red",linestyle="--",label=f"VaR Histórico {intervalo_confianca}%")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=20)
plt.grid(True)

vol_h = dados.std()

vol_h = vol_h

VaR_H = -(montante * z * vol_h)

print(f"O VaR Paramétrico Histórico é:{VaR_H}")
print(f'O valor crítico Z é{z}')

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR Paramétrico Simples {intervalo_confianca}%")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=20)
plt.grid(True)

plt.figure(figsize=(20,10))
ax = plt.gca()
plt.plot(dados,label="Variação dos Retornos",color="blue")
plt.xlabel('Data',fontsize=20)
plt.ylabel('Retornos',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

SMA = dados.rolling(window=30).std()

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue")
plt.plot(SMA, label="Média Móvel Simples",color="black")
plt.xlabel('Data',fontsize=20)
plt.ylabel('Retornos',fontsize=15)
plt.legend(fontsize=20)
plt.grid(True)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.style.use('Solarize_Light2')
plt.show()

print(f"A volatilidade da média móvel é: {SMA}")

vol_SMA = SMA.iloc[-1]

VaR_SMA = -(vol_SMA * z * montante)

print(f"O VaR para a média móvel é:{VaR_SMA}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_SMA/montante),color="green",linestyle="--",label=f"VaR SMA {intervalo_confianca}%")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=20)
plt.grid(True)

lamb1 = 0.05
lamb2 = 0.08
lamb3 = 0.2
EWMA1 = dados.ewm(alpha=lamb1).std()
EWMA2 = dados.ewm(alpha=lamb2).std()
EWMA3 = dados.ewm(alpha=lamb3).std()

EWMA1.dropna()
EWMA2.dropna()
EWMA3.dropna()

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue",alpha=0.3)
plt.plot(SMA, label="Média Móvel Simples",color="black")
plt.plot(EWMA1, label="EWMA=0.95", color="red")
plt.xlabel('Data',fontsize=20)
plt.ylabel('Volatilidade',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

print(f"A volatilidade do EWMA é: {EWMA1.mean()}")

vol_ewma = EWMA1.mean()

VaR_EWMA = -(vol_ewma * z * montante)

print(f"O VaR para o EWMA é:{VaR_EWMA}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_SMA/montante),color="green",linestyle="--",label=f"VaR SMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA/montante),color="purple",linestyle="--",label=f"VaR EWMA = 0.95")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=20)
plt.grid(True)

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue",alpha=0.3)
plt.plot(SMA, label="Média Móvel Simples",color="black",linewidth=2)
plt.plot(EWMA1, label="EWMA=0.95", color="red",linewidth=2)
plt.plot(EWMA2, label="EWMA=0.92", color="purple",linestyle="--",linewidth=2)
plt.plot(EWMA3, label="EWMA=0.80", color="orange",linestyle=":",linewidth=2)
plt.xlabel('Data',fontsize=20)
plt.ylabel('Volatilidade',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

r_sqred = np.sqrt(dados ** 2)
r_sqred = r_sqred.dropna()

ewma_mean = (EWMA1)
ewma_mean = ewma_mean.dropna()

mae = np.mean(np.abs(r_sqred - ewma_mean))
print(f"Mean Absolute Error: {mae}")

mse = np.mean((r_sqred - ewma_mean)**2)
rmse = np.sqrt(mse)
rmse

residuos_absolutos = r_sqred - ewma_mean
residuos_absolutos = residuos_absolutos.dropna()
plt.figure(figsize=(15, 8))
plt.scatter(ewma_mean, residuos_absolutos,color='r',alpha=1)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.style.use('Solarize_Light2')
plt.show()

r_sqred, ewma_mean = r_sqred.align(ewma_mean, join='inner', axis=0)
X = sm.add_constant(ewma_mean)
y = r_sqred
model = sm.OLS(y, X).fit()

residuos_ols = model.resid
residuos_ols
plt.figure(figsize=(8, 6))
plt.scatter(ewma_mean, residuos_ols)
plt.style.use('Solarize_Light2')
plt.axhline(y=0,color="r")
plt.show()

var_residuos = np.var(residuos_absolutos)
residuos_ajustados = residuos_absolutos / np.sqrt(var_residuos)
HRMSE = np.sqrt(np.mean((1 / (var_residuos))**2))
HRMSE

HMAE = np.mean(np.abs(residuos_absolutos) / np.sqrt(var_residuos))
HMAE

def ewma(lambd, series):
    smoothed = np.zeros_like(series)
    smoothed[0] = series[0]
    for t in range(1, len(series)):
        smoothed[t] = lambd * series[t] + (1 - lambd) * smoothed[t - 1]
    return smoothed


def HRMSE(y_true, y_pred):
    return np.sqrt(np.mean((1 - (y_true / y_pred)) ** 2))


def HMAE(y_true, y_pred):
    return np.mean(np.abs(1 - (y_true / y_pred)))


def objectivo(lambda_inicial,y_true):

    y_pred = ewma(y_true, lambda_inicial)


    hrmse = HRMSE(y_true, y_pred)
    hmae = HMAE(y_true, y_pred)


    return 0.5 * hrmse + 0.5 * hmae


y_true = r_sqred.values


lambda_inicial = 0.3


lambda_otimizado = minimize(objectivo, lambda_inicial, bounds=[(0, 1)],args=(y_true))

resultado = lambda_otimizado.x[0]
print(f"O Lambda otimizado Heterocedástico é: {resultado}")

EWMA_Hetero = dados.ewm(alpha=resultado).std()

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue",alpha=0.3)
plt.plot(EWMA_Hetero, label=f"EWMA={(1-resultado).round(2)}", color="red")
plt.xlabel('Data',fontsize=20)
plt.ylabel('Volatilidade',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=12)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

print(f"A volatilidade do EWMA controlado para Heterocedasticidade é: {EWMA_Hetero.mean()}")

vol_ewma_hetero = EWMA_Hetero.mean()

VaR_EWMA_Hetero = -(vol_ewma_hetero * z * montante)

print(f"O VaR para o EWMA Heterocedastico é:{VaR_EWMA_Hetero}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_SMA/montante),color="green",linestyle="--",label=f"VaR SMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA/montante),color="purple",linestyle="--",label=f"VaR EWMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA_Hetero/montante),color="orange",linestyle="--",label=f"VaR EWMA Hetero {(1-resultado).round(2)}%")
plt.style.use('Solarize_Light2')
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.legend(fontsize=15)
plt.grid(True)

def HRMSE_Har(y_true, y_pred):
    return np.sqrt(np.mean((1/ (y_true - y_pred)) ** 2))


def HMAE_Har(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred) / np.sqrt((y_true - y_pred).std()))


def objectivo(lambda_inicial,y_true):

    y_pred = ewma(y_true, lambda_inicial)


    hrmse = HRMSE_Har(y_true, y_pred)
    hmae = HMAE_Har(y_true, y_pred)


    return 0.5 * hrmse + 0.5 * hmae


y_true = r_sqred.values


lambda_inicial = 0.95


lambda_otimizado_harmonizado = minimize(objectivo, lambda_inicial, bounds=[(0, 1)],args=(y_true))

resultado_harmo = lambda_otimizado_harmonizado.x[0]
print(f"O Lambda otimizado por Harmonização é: {resultado_harmo}")

EWMA_Harmo = dados.ewm(alpha=resultado_harmo).std()

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue",alpha=0.3)
plt.plot(EWMA_Harmo, label=f"EWMA={(1-resultado_harmo).round(2)}", color="red")
plt.title('Volatilidade por Média Móvel e EWMA do IBOV')
plt.xlabel('Data')
plt.ylabel('Volatilidade')
plt.legend()
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

print(f"A volatilidade do EWMA Harmonizado é: {EWMA_Harmo.std()}")

vol_ewma_harmo = EWMA_Harmo.mean()

VaR_EWMA_Harmo = -(vol_ewma_harmo * z * montante)

print(f"O VaR para o EWMA Harmonizado é:{VaR_EWMA_Harmo}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA/montante),color="purple",linestyle="--",label=f"VaR EWMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA_Hetero/montante),color="orange",linestyle="--",label=f"VaR EWMA Hetero {(1-resultado).round(2)}%")
plt.axvline(x=(VaR_EWMA_Harmo/montante),color="green",linestyle="--",label=f"VaR EWMA Harmo {(1-resultado_harmo).round(2)}%")
plt.style.use('Solarize_Light2')
plt.title('Distribuição dos Retornos do IBOV e VaR')
plt.xlabel('Retornos')
plt.ylabel('Frequencia')
plt.legend()
plt.grid(True)

plt.figure(figsize=(20,10))
ax = plt.gca()
plt.plot(dados, color="blue")
ax.axvspan(pd.Timestamp('2020-01-01'), pd.Timestamp('2020-06-30'), color='red', alpha=0.3, label='Guerra da Ucrânia')
ax.axvspan(pd.Timestamp('2022-01-01'), pd.Timestamp('2023-03-24'), color='purple', alpha=0.3, label='Boom da IA')


plt.xlabel('Data', fontsize=20)
plt.ylabel('Retornos', fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.legend(fontsize=16)
plt.show()

def plot_normal_curves(dados, means, stds, colors):
    plt.figure(figsize=(20, 10))
    plt.hist(dados, bins=50, edgecolor="black", alpha=0.7, density=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)

    for mean, std, color in zip(means, stds, colors):
        p = norm.pdf(x, mean, std)
        plt.plot(x, p, linewidth=2, color=color, label=f'Média: {mean:.3f}, Desvio Padrão: {std:.3f}')

    plt.xlabel("Desvios Padrões dos Retornos", fontsize=20)
    plt.ylabel("Frequencia", fontsize=20)
    plt.tick_params(axis='y', labelsize=20)
    plt.tick_params(axis='x', labelsize=20)
    plt.style.use('Solarize_Light2')
    plt.legend(fontsize=15)
    plt.show()


means = [dados.mean(), -0.1, 0.1,-0.15,0.15]
stds = [dados.std(),dados.std(),dados.std(),dados.std(),dados.std()]
colors = ['black', 'red', 'blue','green','purple']

plot_normal_curves(dados, means, stds, colors)

garch = arch_model(dados,vol="Garch", p=1,q=1,dist="normal")
f_garch = garch.fit(disp="off")

previsão_garch = f_garch.forecast()

print(f_garch.params)
print(f_garch.summary())
print(previsão_garch)

f_garch.plot(annualize="D")
plt.show()
previsao = f_garch.forecast(start='31-12-2024',method='simulation',horizon=10)
print(previsao.residual_variance.dropna().head())

modelo_garch = (f_garch.conditional_volatility)

print(f"A Volatilidade Média do Modelo GARCH é:{modelo_garch.mean()}")

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue",alpha=0.3)
plt.plot(modelo_garch,label="Volatilidade GARCH",color="blue")
plt.xlabel('Data',fontsize=20)
plt.ylabel('Volatilidade',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

vol_GARCH = 0.03

VaR_GARCH = -(vol_GARCH * z * montante)

print(f"O VaR para o EWMA Harmonizado é:{VaR_GARCH}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA/montante),color="purple",linestyle="--",label=f"VaR EWMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA_Hetero/montante),color="orange",linestyle="--",label=f"VaR EWMA Hetero {(1-resultado).round(2)}%")
plt.axvline(x=(VaR_GARCH/montante),color="blue",linestyle="--",label=f"VaR GARCH")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)

garch_l = arch_model(dados,p=1,q=1,o=1,dist="normal")
l_garch = garch_l.fit(disp="off")

previsão_garch_l = l_garch.forecast()

print(l_garch.params)
print(l_garch.summary())
print(previsão_garch_l)

l_garch.plot(annualize="D")
plt.show()

modelo_garch_alavancado = (l_garch.conditional_volatility)

print(f"A Volatilidade Média do Modelo GARCH é:{modelo_garch_alavancado.mean()}")

plt.figure(figsize=(20,10))
plt.plot(dados, label="Variação dos Retornos", color="blue",alpha=0.3)
plt.plot(modelo_garch_alavancado,label="Volatilidade GARCH com Alavancagem",color="blue")
plt.xlabel('Data',fontsize=20)
plt.ylabel('Volatilidade',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)
plt.style.use('Solarize_Light2')
plt.show()

vol_GARCH_alavancado = 0.031

VaR_GARCH_alavancado = -(vol_GARCH_alavancado * z * montante)

print(f"O VaR para o EWMA Harmonizado é:{VaR_GARCH_alavancado}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA/montante),color="purple",linestyle="--",label=f"VaR EWMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA_Hetero/montante),color="orange",linestyle="--",label=f"VaR EWMA Hetero {(1-resultado).round(2)}%")
plt.axvline(x=(VaR_GARCH_alavancado/montante),color="blue",linestyle="--",label=f"VaR GARCH com Alavancagem")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)

N = norm.cdf

def obj(Ticker):
  objeto = yf.Ticker(Ticker)
  return objeto

def call(Ticker):
  objeto = yf.Ticker(Ticker)
  termino = objeto.options[0]
  option_chain = objeto.option_chain(termino)
  calls = option_chain.calls
  return calls

def BS_CALL(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * N(d1) - K * np.exp(-r*T)* N(d2)

def BS_PUT(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    return K*np.exp(-r*T)*N(-d2) - S*N(-d1)


def implied_vol(opt_value, S, K, T, r, type_='call'):

    def call_obj(sigma):
        return abs(BS_CALL(S, K, T, r, sigma) - opt_value)

    if type_ == 'call':
        res = minimize_scalar(call_obj, bounds=(0.01,100), method='bounded')
        return res.x
    else:
        raise ValueError("type_ must be 'put' or 'call'")

r = 0.0475

tticker = "NVDA"

ivs = []

objeto = obj(Ticker=tticker)

calls = call(Ticker=tticker)
calls['mid'] = (calls['bid'] + calls['ask']) / 2
calls['Time'] = (dt.datetime.strptime(objeto.options[0], '%Y-%m-%d') - dt.datetime.now()).days / 255

preco = objeto.history(period="1d")["Close"].iloc[0]
preco

for row in calls.itertuples():
    iv = implied_vol(row.ask, preco, row.strike, row.Time, r)
    ivs.append(iv)

preco

plt.figure(figsize=(20,10))
plt.scatter(calls.strike, ivs, label='Black-Scholes-Merton',s=70)
plt.scatter(preco,min(ivs),color='r',s=100,label="Preço Corrente\Min Vol")
plt.axvline(preco,color='r',linestyle='--',alpha=0.5)
plt.axhline(y=min(ivs),color='r',linestyle='--',alpha=0.5)
plt.text(preco, min(ivs), f'{round(preco,2)}', color='red', ha='left',va="top",fontsize=15)
plt.text(-15, min(ivs), f'{min(ivs).round(2)}', color='red', ha='left',va="top",fontsize=15)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.xlabel("Strike Prices",fontsize=20)
plt.ylabel("Volatilidade Implícita",fontsize=20)
plt.style.use('Solarize_Light2')
plt.legend(fontsize=15)

plt.figure(figsize=(20,10))
plt.scatter(calls.strike, ivs, label='Black-Scholes-Merton')
plt.scatter(calls.strike, calls.impliedVolatility, label='Bloomberg')
plt.scatter(preco,min(ivs),color='orange',s=100,label="Preço Corrente\Min Vol - Bloomberg")
plt.axvline(preco,color='orange',linestyle='--',alpha=0.5)
plt.axhline(y=min(calls.impliedVolatility),color='orange',linestyle='--',alpha=0.5)
plt.text(preco+2, min(ivs),f'{round(preco,2)}', color='orange', ha='left',va="top",fontsize=15)
plt.text(-15, min(calls.impliedVolatility), f'{round(min(calls.impliedVolatility),2)}', color='orange', ha='left',va="top",fontsize=15)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.xlabel("Strike Prices",fontsize=20)
plt.ylabel("Volatilidade Implícita",fontsize=20)
plt.style.use('Solarize_Light2')
plt.legend(fontsize=15)

vol_BSM = 0.059

VaR_BSM = -(vol_BSM * z * montante)

print(f"O VaR para o Volatility Smile é:{VaR_BSM}")

plt.figure(figsize=(20,10))
plt.hist(dados,bins=50,edgecolor="black",alpha=0.7)
plt.axvline(x=(VaR_H/montante),color="red",linestyle="--",label=f"VaR {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA/montante),color="purple",linestyle="--",label=f"VaR EWMA {intervalo_confianca}%")
plt.axvline(x=(VaR_EWMA_Hetero/montante),color="orange",linestyle="--",label=f"VaR EWMA Hetero {(1-resultado).round(2)}%")
plt.axvline(x=(VaR_GARCH_alavancado/montante),color="blue",linestyle="--",label=f"VaR GARCH com Alavancagem")
plt.axvline(x=(VaR_BSM/montante),color="yellow",linestyle="--",label=f"VaR BSM")
plt.style.use('Solarize_Light2')
plt.xlabel('Retornos',fontsize=20)
plt.ylabel('Frequencia',fontsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.legend(fontsize=15)
plt.grid(True)

np.sum(dados < VaR_H/montante)

dias_SMA = np.sum(dados < (VaR_SMA/montante))/len(dados)*100
dias_EWMA = np.sum(dados < (VaR_EWMA/montante))/len(dados)*100
dias_EWMA_Hetero = np.sum(dados < (VaR_EWMA_Hetero/montante))/len(dados)*100
dias_GARCH = np.sum(dados < (VaR_GARCH/montante))/len(dados)*100
dias_GARCH_alavancado = np.sum(dados < (VaR_GARCH_alavancado/montante))/len(dados)*100
dias_BSM = np.sum(dados < (VaR_BSM/montante))/len(dados)*100
print(f'Dias em que o retorno excedeu o VaR SMA: {dias_SMA}')
print(f'Dias em que o retorno excedeu o VaR EWMA: {dias_EWMA}')
print(f'Dias em que o retorno excedeu o VaR HETERO: {dias_EWMA_Hetero}')
print(f'Dias em que o retorno excedeu o VaR GARCH: {dias_GARCH}')
print(f'Dias em que o retorno excedeu o VaR GARCH alavancado: {dias_GARCH_alavancado}')
print(f'Dias em que o retorno excedeu o VaR BSM:{dias_BSM}')

len(dados)
