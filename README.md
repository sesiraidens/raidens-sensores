<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" width="80">

# raidens-sensores

Biblioteca completa de sensores para robotica: IR, ultrassonico, cor, giroscopio, encoders.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-d9333b?style=flat)
![Status](https://img.shields.io/badge/Status-Active-2ea043?style=flat)

</div>

---

## Sobre

O **raidens-sensores** fornece uma biblioteca unificada de sensores para robos. Inclui sensores de linha, distancia, cor, movimento e ambiente.

---

## Sensores Disponiveis

### Deteccao de Linha

| Sensor | Descricao | Uso |
|---|---|---|
| SensorIR | Infravermelho individual | Deteccao de linha/preto |
| MatrizIR | 5 sensores IR | Posicao da linha |

### Distancia

| Sensor | Descricao | Uso |
|---|---|---|
| Ultrassonico | HC-SR04 | Distancia 2cm-400cm |

### Cores e Luminosidade

| Sensor | Descricao | Uso |
|---|---|---|
| SensorCor | TCS34725 | Deteccao de cor RGB |
| SensorLDR | LDR | Luminosidade ambiente |

### Movimento

| Sensor | Descricao | Uso |
|---|---|---|
| MPU6050 | Acelerometro + Giroscopio | Orientacao e movimento |
| Encoder | Encoder de motor | Velocidade e distancia |

### Temperatura e Audio

| Sensor | Descricao | Uso |
|---|---|---|
| SensorTemperatura | LM35 | Temperatura ambiente |
| Buzzer | Buzzer piezoeletrico | Feedback sonoro |

---

## Uso

### Sensor IR

`python
from src.sensores import SensorIR

ir = SensorIR(nome="frontal", limiar=512)
leitura = ir.ler()  # 0=preto, 1=branco
proporcao = ir.ler_proporcao()  # 0.0-1.0
`

### Matriz IR

`python
from src.sensores import MatrizIR

matriz = MatrizIR()
posicao = matriz.calcular_posicao()  # -2 a +2
detecta = matriz.linha_detectada()  # True/False
`

### Ultrassonico

`python
from src.sensores import Ultrassonico

ultra = Ultrassonico(pin_trigger=9, pin_echo=10)
distancia = ultra.medir_cm()
`

### MPU6050

`python
from src.sensores import MPU6050

mpu = MPU6050()
ax, ay, az = mpu.ler_aceleracao()
gx, gy, gz = mpu.ler_giroscopio()
angulo = mpu.ler_angulo()
`

---

## Calibracao

Todos os sensores suportam calibracao:

`python
sensor.calibrar(valor_referencia)
sensor.reset()  # Reseta calibracao
`

---

## Filtragem

Media movel para reduzir ruido:

`python
valor_filtrado = sensor.media_movel(valor_bruto, janela=5)
`

---

## Equipe

**RAIDENS - SESI Aluminio 192**

Desenvolvido para uso interno da equipe. Licenciado sob MIT.