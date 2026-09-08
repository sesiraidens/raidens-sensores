"""
Biblioteca de sensores para robotica.

Contem drivers e utilitarios para todos os sensores
usados nos robos da RAIDENS.
"""
import time
import math


class SensorBase:
    """
    Classe base para todos os sensores.
    
    Fornece funcionalidade comum como calibracao e filtragem.
    """
    
    def __init__(self, nome, pin=None):
        self.nome = nome
        self.pin = pin
        self.calibrado = False
        self.historico = []
        self.tamanho_historico = 10
        
    def ler(self):
        """Le valor do sensor. Deve ser implementado pelas subclasses."""
        raise NotImplementedError
        
    def ler_bruto(self):
        """Le valor bruto sem processamento."""
        return self.ler()
        
    def media_movel(self, valor, janela=5):
        """
        Filtra valor usando media movel.
        
        Args:
            valor: Valor atual
            janela: Tamanho da janela
            
        Returns:
            float: Valor filtrado
        """
        self.historico.append(valor)
        
        if len(self.historico) > self.tamanho_historico:
            self.historico.pop(0)
            
        ultimos = self.historico[-janela:]
        return sum(ultimos) / len(ultimos)
        
    def calibrar(self, valor):
        """Define valor de calibracao."""
        self.valor_calibracao = valor
        self.calibrado = True
        
    def normalizar(self, valor, minimo=0, maximo=1023):
        """Normaliza valor para 0.0 - 1.0."""
        return (valor - minimo) / (maximo - minimo)
        
    def reset(self):
        """Reseta historico."""
        self.historico = []
        self.calibrado = False


class SensorIR(SensorBase):
    """
    Sensor infravermelho para deteccao de linha.
    
    Detecta reflectancia de superficie.
    """
    
    PRETO = 0
    BRANCO = 1
    
    def __init__(self, nome="IR", pin="A0", limiar=512):
        super().__init__(nome, pin)
        self.limiar = limiar
        
    def ler(self):
        """Le e retorna 0 (preto) ou 1 (branco)."""
        import random
        bruto = random.randint(0, 1023)
        return self.BRANCO if bruto > self.limiar else self.PRETO
        
    def ler_bruto(self):
        """Le valor bruto (0-1023)."""
        import random
        return random.randint(0, 1023)
        
    def ler_proporcao(self):
        """Le e retorna proporcão (0.0 - 1.0)."""
        import random
        bruto = random.randint(0, 1023)
        return bruto / 1023.0
        
    def detectar_parede(self):
        """Detecta se ha parede (objeto proximo)."""
        return self.ler() == self.PRETO


class MatrizIR:
    """
    Matriz de 5 sensores IR para deteccao de linha.
    
    Calcula posicao da linha relativa ao centro.
    """
    
    def __init__(self, pins=None):
        if pins is None:
            pins = ["A0", "A1", "A2", "A3", "A4"]
            
        self.sensores = [SensorIR(f"IR{i}", pin) for i, pin in enumerate(pins)]
        self.pesos = [-2, -1, 0, 1, 2]
        
    def ler_todos(self):
        """Le todos os sensores."""
        return [s.ler() for s in self.sensores]
        
    def calcular_posicao(self):
        """
        Calcula posicao da linha (-2 a +2).
        
        Returns:
            float: Posicao, 0 = centro
        """
        leituras = self.ler_todos()
        
        soma_pesos = 0
        soma_leituras = 0
        
        for i, leitura in enumerate(leituras):
            if leitura == SensorIR.PRETO:
                soma_pesos += self.pesos[i]
                soma_leituras += 1
                
        if soma_leituras == 0:
            return 0
            
        return soma_pesos / soma_leituras
        
    def linha_detectada(self):
        """Verifica se ha linha sob os sensores."""
        return any(s.ler() == SensorIR.PRETO for s in self.sensores)
        
    def calibrar_todos(self):
        """Calibra todos os sensores."""
        for s in self.sensores:
            s.calibrar(s.ler_bruto())


class Ultrassonico(SensorBase):
    """
    Sensor ultrassonico HC-SR04.
    
    Mede distancia usando tempo de eco sonoro.
    """
    
    VELOCIDADE_SOM = 343  # m/s
    
    def __init__(self, nome="HC-SR04", pin_trigger=9, pin_echo=10):
        super().__init__(nome)
        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        self.distancia_maxima = 400  # cm
        
    def ler(self):
        """Le distancia em cm."""
        import time
        import random
        
        time.sleep(0.00001)
        
        tempo_inicio = time.time()
        tempo_fim = tempo_inicio + 0.04
        
        while time.time() < tempo_fim:
            pass
            
        tempo_decorrido = time.time() - tempo_inicio
        distancia = (tempo_decorrido * self.VELOCIDADE_SOM) / 2
        
        distancia += random.uniform(-0.5, 0.5)
        
        return round(distancia, 2)
        
    def ler_metros(self):
        """Le distancia em metros."""
        return self.ler() / 100
        
    def dentro_da_faixa(self, minimo, maximo):
        """Verifica se distancia esta dentro da faixa."""
        dist = self.ler()
        return minimo <= dist <= maximo
        
    def parede_detectada(self, distancia_segura=20):
        """Detecta se ha parede proxima."""
        return self.ler() < distancia_segura


class SensorCor(SensorBase):
    """
    Sensor de cor TCS34725.
    
    Detecta cores RGB e luminosidade.
    """
    
    def __init__(self, nome="TCS34725", endereco=0x29):
        super().__init__(nome)
        self.endereco = endereco
        
    def ler(self):
        """Le cor RGB."""
        return self.ler_rgb()
        
    def ler_rgb(self):
        """Retorna tupla (r, g, b)."""
        import random
        return (random.randint(0, 255), 
                random.randint(0, 255), 
                random.randint(0, 255))
                
    def ler_luminosidade(self):
        """Retorna luminosidade (0-65535)."""
        import random
        return random.randint(0, 65535)
        
    def detectar_cor(self):
        """Detecta cor predominante."""
        r, g, b = self.ler_rgb()
        
        cores = {
            "vermelho": abs(r - 255) + abs(g) + abs(b),
            "verde": abs(r) + abs(g - 255) + abs(b),
            "azul": abs(r) + abs(g) + abs(b - 255),
            "amarelo": abs(r - 255) + abs(g - 255) + abs(b),
            "branco": abs(r - 255) + abs(g - 255) + abs(b - 255),
            "preto": abs(r) + abs(g) + abs(b),
        }
        
        return min(cores, key=cores.get)
        
    def calibrar_branco(self):
        """Calibra referencia de branco."""
        self.referencia = self.ler_rgb()
        self.calibrado = True


class MPU6050(SensorBase):
    """
    Acelerometro e giroscopio MPU6050.
    
    Mede aceleracao e velocidade angular.
    """
    
    def __init__(self, nome="MPU6050", endereco=0x68):
        super().__init__(nome)
        self.endereco = endereco
        self.offset_giroscopio = 0
        
    def ler(self):
        """Le dados completos."""
        return {
            "aceleracao": self.ler_aceleracao(),
            "giroscopio": self.ler_giroscopio()
        }
        
    def ler_aceleracao(self):
        """Retorna (ax, ay, az) em g."""
        import random
        return (round(random.uniform(-0.1, 0.1), 3),
                round(random.uniform(-0.1, 0.1), 3),
                round(random.uniform(0.9, 1.1), 3))
                
    def ler_giroscopio(self):
        """Retorna (gx, gy, gz) em graus/s."""
        import random
        return (round(random.uniform(-1, 1), 3),
                round(random.uniform(-1, 1), 3),
                round(random.uniform(-1, 1) - self.offset_giroscopio, 3))
                
    def ler_angulo(self):
        """Calcula angulo baseado no acelerometro."""
        ax, ay, az = self.ler_aceleracao()
        angulo_x = math.degrees(math.atan2(ay, az))
        angulo_y = math.degrees(math.atan2(-ax, az))
        return (angulo_x, angulo_y)
        
    def calibrar_giroscopio(self, amostras=100):
        """Calibra offset do giroscopio."""
        import time
        soma = 0
        for _ in range(amostras):
            _, _, gz = self.ler_giroscopio()
            soma += gz
            time.sleep(0.01)
        self.offset_giroscopio = soma / amostras


class Encoder(SensorBase):
    """
    Encoder de motor para medicao de velocidade.
    """
    
    def __init__(self, nome="Encoder", ppr=20, pin_a=2, pin_b=3):
        super().__init__(nome)
        self.ppr = ppr
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.contador = 0
        self.circunferencia_roda = 21.99  # cm
        
    def ler(self):
        """Retorna velocidade em cm/s."""
        return self.velocidade(0.1)
        
    def incrementar(self):
        """Incrementa contador."""
        self.contador += 1
        
    def decrementar(self):
        """Decrementa contador."""
        self.contador -= 1
        
    def velocidade(self, tempo_segundos):
        """Calcula velocidade em cm/s."""
        revolucoes = self.contador / self.ppr
        distancia = revolucoes * self.circunferencia_roda
        self.contador = 0
        return distancia / tempo_segundos
        
    def distancia(self):
        """Calcula distancia total em cm."""
        revolucoes = self.contador / self.ppr
        return revolucoes * self.circunferencia_roda
        
    def reset(self):
        """Reseta contador."""
        self.contador = 0


class SensorLDR(SensorBase):
    """
    Sensor de luminosidade LDR.
    """
    
    def __init__(self, nome="LDR", pin="A5"):
        super().__init__(nome, pin)
        
    def ler(self):
        """Le luminosidade (0-1023)."""
        import random
        return random.randint(0, 1023)
        
    def luminosidade_percentual(self):
        """Retorna luminosidade em percentual."""
        return self.ler() / 10.23
        
    def escuro(self, limiar=200):
        """Verifica se esta escuro."""
        return self.ler() < limiar
        
    def claro(self, limiar=800):
        """Verifica se esta claro."""
        return self.ler() > limiar


class SensorTemperatura(SensorBase):
    """
    Sensor de temperatura LM35.
    """
    
    def __init__(self, nome="LM35", pin="A4"):
        super().__init__(nome, pin)
        
    def ler(self):
        """Le temperatura em graus Celsius."""
        import random
        return round(random.uniform(20, 35), 1)
        
    def ler_fahrenheit(self):
        """Le temperatura em Fahrenheit."""
        celsius = self.ler()
        return celsius * 9/5 + 32
        
    def quente(self, limiar=30):
        """Verifica se esta quente."""
        return self.ler() > limiar


class Buzzer(SensorBase):
    """
    Buzzer para feedback sonoro.
    """
    
    def __init__(self, nome="Buzzer", pin=8):
        super().__init__(nome, pin)
        
    def ler(self):
        """Retorna estado atual."""
        return False
        
    def tone(self, frequencia, duracao=200):
        """Toca uma nota."""
        print(f"Tone: {frequencia}Hz por {duracao}ms")
        
    def beep(self, duracao=100):
        """Emite beep."""
        self.tone(1000, duracao)
        
    def alarme(self, repeticoes=3):
        """Emite alarme."""
        for _ in range(repeticoes):
            self.tone(1000, 200)
            time.sleep(0.1)
            self.tone(500, 200)
            time.sleep(0.1)
