<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="140">

# raidens-sensores

**Catálogo de sensores para robótica em Python, com calibração e filtragem de ruído**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-2EA043?style=flat-square)
![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-D9333B?style=flat-square)

[Sobre](#sobre) · [Instalação](#instalação) · [Sensores](#sensores-disponíveis) · [Uso](#uso)

</div>

---

## Sobre

O **raidens-sensores** reúne em uma única API todos os sensores que aparecem nos robôs da RAIDENS. Todos herdam de `SensorBase`, então compartilham o mesmo jeito de ler (`ler()`, `ler_bruto()`), calibrar (`calibrar()`, `reset()`) e filtrar (`media_movel()`). Trocar um sensor por outro não exige reaprender nada.

As leituras são simuladas, o que permite testar a lógica do robô no computador antes de ligar o hardware.

## Instalação

```bash
git clone https://github.com/sesiraidens/raidens-sensores.git
cd raidens-sensores
```

Requer apenas Python 3.8 ou superior. Rode os scripts a partir da raiz do repositório.

## Sensores disponíveis

| Categoria | Classe | Hardware | Uso típico |
|---|---|---|---|
| Linha | `SensorIR` | Infravermelho | Detectar preto/branco |
| Linha | `MatrizIR` | 5 sensores IR | Posição da linha (−2 a +2) |
| Distância | `Ultrassonico` | HC-SR04 | 2 cm a 400 cm |
| Cor | `SensorCor` | TCS34725 | Cor RGB e luminosidade |
| Luz | `SensorLDR` | LDR | Claro ou escuro |
| Movimento | `MPU6050` | Acelerômetro + giroscópio | Orientação e inclinação |
| Movimento | `Encoder` | Encoder de roda | Velocidade e distância percorrida |
| Ambiente | `SensorTemperatura` | LM35 | Temperatura em °C e °F |
| Feedback | `Buzzer` | Piezoelétrico | Bipes e alarmes |

## Uso

```python
from src.sensores import SensorIR, MatrizIR, Ultrassonico, MPU6050

ir = SensorIR(nome="frontal", pin="A0", limiar=512)
ir.ler()                       # 0 = preto, 1 = branco
ir.ler_proporcao()             # 0.0 a 1.0

matriz = MatrizIR()
matriz.calcular_posicao()      # -2 (esquerda) a +2 (direita)
matriz.linha_detectada()

ultra = Ultrassonico(pin_trigger=9, pin_echo=10)
ultra.ler()                    # distância em cm
ultra.parede_detectada(distancia_segura=20)

mpu = MPU6050()
ax, ay, az = mpu.ler_aceleracao()
gx, gy, gz = mpu.ler_giroscopio()
```

### Calibração e filtragem

```python
sensor.calibrar(valor_referencia)
sensor.reset()

valor_filtrado = sensor.media_movel(valor_bruto, janela=5)
```

## Estrutura

```text
raidens-sensores/
└── src/
    └── sensores.py   # SensorBase e todas as classes de sensor
```

## Ecossistema RAIDENS

Este repositório faz parte de um conjunto de bibliotecas da equipe. Elas usam os mesmos nomes de classes e convenções, então o que você aprende em uma serve nas outras.

| Repositório | Para quê |
|---|---|
| [`raidens-python`](https://github.com/sesiraidens/raidens-python) | Biblioteca principal em Python: sensores, motores e robôs prontos (seguidor, parede, resgate) |
| [`raidens-arduino`](https://github.com/sesiraidens/raidens-arduino) | As mesmas abstrações em C++ para rodar direto no Arduino |
| [`raidens-motores`](https://github.com/sesiraidens/raidens-motores) | Motores DC, servo, passo, driver L298N e rodas mecanum |
| [`raidens-pid`](https://github.com/sesiraidens/raidens-pid) | Controladores PID, PID avançado, cascata e sintonia Ziegler-Nichols |
| [`raidens-opencv`](https://github.com/sesiraidens/raidens-opencv) | Visão computacional: cores, linhas e navegação por câmera |
| [`raidens-lab`](https://github.com/sesiraidens/raidens-lab) | Calibração interativa de cores em HSV e LAB |
| [`raidens-obr`](https://github.com/sesiraidens/raidens-obr) | Robô completo para a OBR, integrando sensores, motores e missões |
| [`raidens-electronics`](https://github.com/sesiraidens/raidens-electronics) | Cálculos e modelos de componentes eletrônicos |
| [`raidens-3d`](https://github.com/sesiraidens/raidens-3d) | Peças 3D paramétricas geradas em OpenSCAD |
| [`raidens-ros`](https://github.com/sesiraidens/raidens-ros) | Estrutura de nodes e tópicos ROS 2 |
| [`raidens-snippets`](https://github.com/sesiraidens/raidens-snippets) | Trechos de código prontos para copiar e colar |

---

<div align="center">

<img src="https://sesiraidens.github.io/portifolio/assets/logo_color-aNRVU26Y.png" alt="Logo RAIDENS" width="56">

**Equipe RAIDENS** · SESI 192 Alumínio/SP

[![Email](https://img.shields.io/badge/Email-sesiraidens%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:sesiraidens@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-sesiraidens-39E06B?style=flat-square&logo=linktree&logoColor=white)](https://linktr.ee/sesiraidens)
[![GitHub](https://img.shields.io/badge/GitHub-sesiraidens-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/sesiraidens)

<sub>Desenvolvido pela equipe RAIDENS para fins educacionais. Licenciado sob MIT.</sub>

</div>


