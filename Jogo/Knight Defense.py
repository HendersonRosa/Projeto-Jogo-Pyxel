import pyxel
import time
import random
import math

# --- SISTEMA DE ANIMAÇÃO ---
class AnimationSystem:
    @staticmethod
    def draw_stick_figure(x, y, color, frame, scale=1.0, facing_right=True, is_moving=True, is_dashing=False):
        """Desenha um boneco palito animado ou parado"""
        
        if is_dashing: # NOVO: Configurações para o efeito de Dash
            # Boneco alongado para simular velocidade e borrão
            head_size = int(1 * scale)    # Cabeça menor
            body_height = int(12 * scale) # Corpo mais longo (Original: 8)
            arm_length = int(6 * scale)   # Braços mais longos (Original: 4)
            leg_length = int(8 * scale)   # Pernas mais longas (Original: 6)
            is_moving = False             # Desativa a animação de braços/pernas (para ficarem retos)
        else:
            # Configurações normais
            head_size = int(2 * scale)
            body_height = int(8 * scale)
            arm_length = int(4 * scale)
            leg_length = int(6 * scale)
        
        # Cabeça
        pyxel.circ(x, y - body_height - head_size, head_size, color)
        
        # Corpo
        pyxel.line(x, y - body_height, x, y, color)
        
        # Animação de caminhada: somente se estiver se movendo E não estiver dando dash
        if is_moving and not is_dashing:
            arm_swing = math.sin(frame * 0.3) * 2 * scale
            leg_swing = math.sin(frame * 0.3) * 3 * scale
        else:
            arm_swing = 0
            leg_swing = 0
        
        # Direção
        direction = 1 if facing_right else -1
        
        # Braços
        arm_y = y - body_height + 2
        pyxel.line(x, arm_y, x + direction * (arm_length + arm_swing), arm_y - 1, color)
        pyxel.line(x, arm_y, x + direction * (arm_length - arm_swing), arm_y + 1, color)
        
        # Pernas
        leg_start_y = y
        # Se parado, as pernas ficam levemente abertas, se movendo, balançam
        if not is_moving:
             pyxel.line(x, leg_start_y, x + direction * 2, leg_start_y + leg_length, color)
             pyxel.line(x, leg_start_y, x - direction * 2, leg_start_y + leg_length, color)
        else:
            pyxel.line(x, leg_start_y, x + direction * (2 + leg_swing), leg_start_y + leg_length, color)
            pyxel.line(x, leg_start_y, x + direction * (2 - leg_swing), leg_start_y + leg_length, color)


    @staticmethod
    def draw_archer_figure(x, y, color, frame, scale=1.0, facing_right=True, is_moving=True):
        """Desenha um arqueiro com arco"""
        # Desenha boneco base
        AnimationSystem.draw_stick_figure(x, y, color, frame, scale, facing_right, is_moving)
        
        # Arco
        direction = 1 if facing_right else -1
        bow_x = x + direction * 6 * scale
        bow_y = y - 4 * scale
        
        # Arco simples
        pyxel.line(bow_x, bow_y - 3, bow_x, bow_y + 3, 6)
        pyxel.line(bow_x, bow_y - 3, bow_x + direction * 2, bow_y, 6)
        pyxel.line(bow_x, bow_y + 3, bow_x + direction * 2, bow_y, 6)

    @staticmethod
    def draw_boss_figure(x, y, color, frame, scale=1.5, is_moving=True):
        """Desenha o boss maior e mais imponente"""
        # Cabeça maior
        head_size = int(4 * scale)
        body_height = int(12 * scale)
        arm_length = int(6 * scale)
        leg_length = int(8 * scale)
        
        # Cabeça com detalhes
        pyxel.circ(x, y - body_height - head_size, head_size, color)
        pyxel.circ(x, y - body_height - head_size, head_size - 1, 8)  # Contorno vermelho
        
        # Corpo mais grosso
        pyxel.line(x - 1, y - body_height, x - 1, y, color)
        pyxel.line(x, y - body_height, x, y, color)
        pyxel.line(x + 1, y - body_height, x + 1, y, color)
        
        # Animação mais lenta e pesada: somente se estiver se movendo
        if is_moving:
            arm_swing = math.sin(frame * 0.15) * 3 * scale
            leg_swing = math.sin(frame * 0.15) * 2 * scale
        else:
            arm_swing = 0
            leg_swing = 0
        
        # Braços mais grossos
        arm_y = y - body_height + 3
        for i in range(2):
            pyxel.line(x, arm_y + i, x + (arm_length + arm_swing), arm_y - 2 + i, color)
            pyxel.line(x, arm_y + i, x - (arm_length - arm_swing), arm_y + 2 + i, color)
        
        # Pernas mais grossas
        leg_start_y = y
        # Se parado, pernas levemente mais grossas e paradas
        if not is_moving:
            for i in range(2):
                pyxel.line(x + i, leg_start_y, x + 3 + i, leg_start_y + leg_length, color)
                pyxel.line(x - i, leg_start_y, x - 3 - i, leg_start_y + leg_length, color)
        else:
            for i in range(2):
                pyxel.line(x + i, leg_start_y, x + (3 + leg_swing) + i, leg_start_y + leg_length, color)
                pyxel.line(x - i, leg_start_y, x - (3 - leg_swing) - i, leg_start_y + leg_length, color)


class Parede:
    def __init__(self, x, y, w, h, c = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c  

    def draw(self):
        pyxel.blt(0, 0, 2, 0, 0, 256, 144)


class Personagem:
    def __init__(self, x, y, raio, cor, vida, ataque, defesa):
        self.x = x
        self.y = y
        self.raio = 5
        self.cor = 0  # Azul claro para o jogador
        self.cor_original = 4
        self.animation_frame = 0
        self.facing_right = True
        self.last_x = x
        self.is_moving = False 

        self.vida_base = vida
        self.ataque_base = ataque
        self.defesa_base = defesa
        self.bonus_vida = 0
        self.bonus_ataque = 0
        self.bonus_defesa = 0

        self.vida = self.vida_base
        self.ataque = self.ataque_base
        self.defesa = self.defesa_base

        self.dx = 1
        self.dy = 1

        self.attacking = False
        self.attack_frames = 0
        self.last_attack_time = 0
        self.last_dir_x = 1
        self.last_dir_y = 0
        self.targets_hit = set()

        self.dashing = False
        self.dash_speed = 3
        self.dash_duration = 4
        self.dash_cooldown = 4
        self.last_dash_time = -self.dash_cooldown
        self.vx = 0
        self.vy = 0
        self.dash_frames = 0
        self.dano_tempo = 0

    def tomar_dano(self, valor):
        self.vida -= valor
        self.cor = 8  # vermelho indicando dano
        self.dano_tempo = time.time() + 0.15

    def update_animation(self, current_dir_x, current_dir_y): # <-- Recebe direção atual
        # Define se está se movendo
        self.is_moving = current_dir_x != 0 or current_dir_y != 0 or self.dashing
        
        # Atualiza direção baseada no movimento
        if self.x != self.last_x:
            self.facing_right = self.x > self.last_x
        self.last_x = self.x
        
        # Incrementa frame de animação se estiver movendo
        if self.is_moving:
            self.animation_frame += 1

    def draw(self):
        # Lógica de cor de dano
        cor_final = self.cor_original
        if hasattr(self, "dano_tempo") and time.time() < self.dano_tempo:
            cor_final = 8 # Vermelho de dano
        
        # --- LÓGICA DO DASH: Sobrescreve a cor se estiver dashing ---
        if self.dashing:
            cor_final = 7 # Branco para o efeito visual (Risco de dano é ignorado durante o dash)
            
        # Desenha boneco animado
        AnimationSystem.draw_stick_figure(
            self.x, self.y + self.raio, 
            cor_final, 
            self.animation_frame, 
            1.0, 
            self.facing_right,
            self.is_moving,
            is_dashing=self.dashing 
        )

class Inimigo:
    def __init__(self, x, y, vida=25, ataque=20, defesa=5):
        self.x = x
        self.y = y
        self.raio = 5
        self.cor = 10  
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.vx = 0
        self.vy = 0
        self.attacking = False
        self.attack_frames = 0
        self.last_attack_time = 0
        self.last_dir_x = 1
        self.last_dir_y = 0
        self.targets_hit = set()
        self.stun_end_time = 0
        self.cor_dano = 8
        self.dano_tempo = 0
        self.vida = vida
        self.vida_max = vida
        self.animation_frame = 0
        self.facing_right = True
        self.last_x = x
        self.is_moving = False # <--- Estado de movimento

    def tomar_dano(self, valor):
        self.vida -= valor
        self.dano_tempo = time.time() + 0.15  # vermelho por 0.15 s
        self.barra_tempo = time.time() + 0.6

    def update_animation(self):
        # Define se está se movendo (velocidade maior que 0.1)
        self.is_moving = abs(self.vx) > 0.1 or abs(self.vy) > 0.1
        
        # Atualiza direção baseada no movimento
        if self.x != self.last_x:
            self.facing_right = self.x > self.last_x
        self.last_x = self.x
        
        # Incrementa frame de animação se estiver movendo
        if self.is_moving:
            self.animation_frame += 1

    def draw(self):
        # Cor padrão
        cor_atual = self.cor

        # Se estiver stunado, cor branca
        if time.time() < self.stun_end_time:
            cor_atual = 7  # branco
        # Se tomou dano recentemente, cor vermelha
        elif hasattr(self, "dano_tempo") and time.time() < self.dano_tempo:
            cor_atual = 8  # vermelho

        # Desenha boneco animado
        AnimationSystem.draw_stick_figure(
            self.x, self.y + self.raio, 
            cor_atual, self.animation_frame, 
            0.8, self.facing_right,
            self.is_moving
        )
        
        # Barra de vida apenas se tomou dano
        if time.time() < getattr(self, "barra_tempo", 0):
            barra_w, barra_h = 7, 1
            pyxel.rect(self.x - barra_w // 2, self.y - self.raio - 8, barra_w, barra_h, 7)
            pyxel.rect(self.x - barra_w // 2, self.y - self.raio - 8,
                      barra_w * self.vida / self.vida_max, barra_h, 8)
class Projetil:
    def __init__(self, x, y, vx, vy, dano):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dano = dano
        self.raio = 2
        self.remover = False

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if not (0 < self.x < 256 and 0 < self.y < 144):
            self.remover = True

    
    def draw(self):
        # Calcula a direção normalizada
        mag = (self.vx**2 + self.vy**2) ** 0.5 or 1
        nx, ny = self.vx / mag, self.vy / mag

        # Dimensões da flecha
        comprimento = 6  # comprimento da flecha
        espessura = 2   # largura da flecha

        # Posição central
        cx, cy = self.x, self.y

        # Ortogonal para dar espessura
        ortho_x, ortho_y = -ny, nx

        # Calcula os cantos do retângulo
        p1 = (cx - nx * comprimento/2 - ortho_x * espessura/2,
            cy - ny * comprimento/2 - ortho_y * espessura/2)
        p2 = (cx + nx * comprimento/2 - ortho_x * espessura/2,
            cy + ny * comprimento/2 - ortho_y * espessura/2)
        p3 = (cx + nx * comprimento/2 + ortho_x * espessura/2,
            cy + ny * comprimento/2 + ortho_y * espessura/2)
        p4 = (cx - nx * comprimento/2 + ortho_x * espessura/2,
            cy - ny * comprimento/2 + ortho_y * espessura/2)

        # Desenha a flecha como 4 linhas conectadas (retângulo)
        cor = 7  # branco (pode trocar)
        pyxel.line(*p1, *p2, cor)
        pyxel.line(*p2, *p3, cor)
        pyxel.line(*p3, *p4, cor)
        pyxel.line(*p4, *p1, cor)

class Arqueiro(Inimigo):
    def __init__(self, x, y, vida=20, ataque=35, defesa=3):
        super().__init__(x, y, vida, ataque, defesa)
        self.raio = 5
        self.cor = 6  # Cor diferente para arqueiros
        self.projetil_cooldown = 2.0
        self.last_shot_time = 0
        self.projetis = []
        self.vida_max = vida
        
    def atirar(self, target_x, target_y):
        """Cria e lança um projetil na direção do alvo."""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx**2 + dy**2)**0.5
        
        # Velocidade do projétil
        speed = 2.5 
        
        # velocidade 
        if dist != 0:
            vx = dx / dist * speed
            vy = dy / dist * speed
        else:
            vx, vy = speed, 0 

        # Cria o projétil na lista de projéteis do arqueiro
        self.projetis.append(Projetil(self.x, self.y, vx, vy, self.ataque))


    def update(self, player, jogo_ref): # <--- Adiciona referência ao Jogo
        # Atualiza animação
        self.update_animation()
        
        # --- se estiver stunado: comportamento igual aos inimigos normais ---
        if time.time() < self.stun_end_time:
            # continua movendo pela inércia, aplica atrito e mantém dentro dos limites
            self.x += self.vx
            self.y += self.vy
            self.vx *= 0.9
            self.vy *= 0.9
            jogo_ref.check_wall_collision(self) # <--- NOVO: Aplica colisão
            return  # não executa o resto (não atira nem busca o jogador)

        # --- comportamento normal quando NÃO está stunado ---
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2)**0.5
        if dist != 0:
            nx, ny = dx / dist, dy / dist
        else:
            nx, ny = 0, 0

        follow_speed = 0.5
        dist_min = 40  # distância mínima que ele tenta manter
        dist_max = 60  # distância máxima para começar a se aproximar

        if dist < dist_min:
            # recua do jogador
            self.vx += -nx * 0.05
            self.vy += -ny * 0.05
        elif dist > dist_max:
            # aproxima do jogador
            self.vx += nx * 0.05
            self.vy += ny * 0.05
        else:
            # mantém posição, só fricção
            self.vx *= 0.85
            self.vy *= 0.85

        # Limita velocidade
        self.vx = max(-follow_speed, min(self.vx, follow_speed))
        self.vy = max(-follow_speed, min(self.vy, follow_speed))

        # Atualiza posição
        self.x += self.vx
        self.y += self.vy

        jogo_ref.check_wall_collision(self) # <--- NOVO: Aplica colisão

        # Atirar se estiver dentro do alcance
        if dist <= 80 and time.time() - self.last_shot_time >= self.projetil_cooldown:
            self.atirar(player.x, player.y)
            self.last_shot_time = time.time()

        # Atualiza projéteis
        for p in self.projetis[:]:
            p.update()
            if p.remover:
                self.projetis.remove(p)

    def draw(self):
        # Cor padrão
        cor_atual = self.cor

        # Se estiver stunado, cor branca
        if time.time() < self.stun_end_time:
            cor_atual = 7  # branco
        # Se tomou dano recentemente, cor vermelha
        elif hasattr(self, "dano_tempo") and time.time() < self.dano_tempo:
            cor_atual = 8  # vermelho

        # Desenha arqueiro animado
        AnimationSystem.draw_archer_figure(
            self.x, self.y + self.raio, 
            cor_atual, self.animation_frame, 
            0.8, self.facing_right,
            self.is_moving
        )
        
        # Barra de vida apenas se tomou dano
        if time.time() < getattr(self, "barra_tempo", 0):
            barra_w, barra_h = 7, 1
            pyxel.rect(self.x - barra_w // 2, self.y - self.raio - 8, barra_w, barra_h, 7)
            pyxel.rect(self.x - barra_w // 2, self.y - self.raio - 8,
                      barra_w * self.vida / self.vida_max, barra_h, 8)

        # Desenha projéteis
        for p in self.projetis:
            p.draw()

class AtaqueChao:
    def __init__(self, x, y, largura=30, altura=10, duracao=0.8, dano=30, aviso_duracao=0.5):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.duracao = duracao
        self.dano = dano
        self.inicio = time.time()
        self.remover = False
        self.aviso_duracao = aviso_duracao  # tempo que fica piscando
        self.dano_ativo = False

    def update(self, player):
        tempo_passado = time.time() - self.inicio

        # Ativa dano somente após aviso
        if not self.dano_ativo and tempo_passado >= self.aviso_duracao:
            self.dano_ativo = True

        # Remove ataque após duração total
        if tempo_passado > self.duracao:
            self.remover = True

        # Aplica dano somente se o ataque estiver ativo
        if self.dano_ativo:
            if (self.x <= player.x <= self.x + self.largura and
                self.y <= player.y <= self.y + self.altura):
                player.tomar_dano(self.dano)
                self.remover = True  # só acerta uma vez

    def draw(self):
        # Durante aviso, pisca entre vermelho e branco
        tempo_passado = time.time() - self.inicio
        if not self.dano_ativo:
            cor = 8 if int(tempo_passado * 8) % 2 == 0 else 7  # piscando
        else:
            cor = 8  # vermelho quando ativo
        pyxel.rect(self.x, self.y, self.largura, self.altura, cor)


class AtaqueCircular:
    def __init__(self, boss, raio=25, duracao=0.8, dano=40, aviso_duracao=1.5, dano_cooldown=0.2):
        self.boss = boss
        self.raio = raio
        self.duracao = duracao
        self.dano = dano
        self.inicio = time.time()
        self.remover = False
        self.aviso_duracao = aviso_duracao  # Aumentado para 1.5s para dar mais tempo
        self.dano_ativo = False
        self.last_dano_frame = pyxel.frame_count
        self.dano_intervalo = 30  # Aumentado para dar mais tempo entre danos
        self.ja_causou_dano = False  # Para causar dano apenas uma vez

    def update(self, player):
        tempo_passado = time.time() - self.inicio
        
        # Ativa o dano após o período de aviso
        if not self.dano_ativo and tempo_passado >= self.aviso_duracao:
            self.dano_ativo = True
        
        # Remove o ataque após a duração total
        if tempo_passado > self.aviso_duracao + self.duracao:
            self.remover = True
            return

        # Aplica dano apenas uma vez quando o ataque está ativo
        if self.dano_ativo and not self.ja_causou_dano:
            dx = player.x - self.boss.x
            dy = player.y - self.boss.y
            dist = (dx**2 + dy**2)**0.5
            
            # Verifica se o jogador está dentro da área de dano
            if dist <= self.raio + player.raio:
                player.tomar_dano(self.dano)
                self.ja_causou_dano = True

    def draw(self):
        tempo_passado = time.time() - self.inicio
        
        if not self.dano_ativo:
            # Fase de aviso: pisca em vermelho/amarelo
            cor = 8 if int(tempo_passado * 6) % 2 == 0 else 10
        else:
            # Fase de dano: vermelho sólido
            cor = 8
        
        # Desenha o círculo de área de efeito
        pyxel.circb(self.boss.x, self.boss.y, self.raio, cor)
        
        # Desenha círculos internos para melhor visualização
        for r in range(5, self.raio, 10):
            pyxel.circb(self.boss.x, self.boss.y, r, cor)


class Boss(Inimigo):
    def __init__(self, x, y, vida=300, ataque=40, defesa=10):
        super().__init__(x, y, vida, ataque, defesa)
        self.raio = 10
        self.cor = 9  # Cor especial para o boss
        self.vida_max = vida
        self.ataques_chao = []
        self.ataque_especial_cooldown = 3.0
        self.last_especial_time = 0
        self.modo_agressivo = False
        self.spawn_stages = [0.75, 0.5, 0.25]  # percentuais de vida para gerar inimigos
        self.animation_frame = 0
        self.last_x = x
        self.is_moving = False # <--- Estado de movimento

    def update_animation(self):
        # Define se está se movendo (velocidade maior que 0.1)
        self.is_moving = abs(self.vx) > 0.1 or abs(self.vy) > 0.1
        
        # Atualiza frame de animação (mais lento que inimigos normais)
        if self.is_moving:
            self.animation_frame += 0.5

    def tomar_dano(self, valor, jogo=None):
        self.vida -= valor
        self.dano_tempo = time.time() + 0.15  # vermelho por 0.15s

        # Checa se atingiu algum estágio de vida
        if jogo is not None:
            for stage in self.spawn_stages[:]:  # itera sobre cópia
                if self.vida <= self.vida_max * stage:
                    # gera 2 inimigos normais
                    for _ in range(2):
                        x = random.randint(20, 236)
                        y = random.randint(20, 124)
                        # Usa a classe Inimigo, que agora é amarela
                        jogo.li.append(Inimigo(x, y)) 
                    # gera 1 arqueiro
                    x = random.randint(20, 236)
                    y = random.randint(20, 124)
                    jogo.li.append(Arqueiro(x, y))
                    
                    self.spawn_stages.remove(stage)  # garante que só ocorre uma vez

    def update(self, player, jogo_ref): # <--- Adiciona referência ao Jogo
        # Atualiza animação
        self.update_animation()
        
        # Ativa modo agressivo se vida < 50%
        self.modo_agressivo = self.vida < self.vida_max / 2

        # Movimentação
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2)**0.5
        nx, ny = (dx / dist, dy / dist) if dist != 0 else (0, 0)
        speed = 0.5 if self.modo_agressivo else 0.3

        if dist > 30:
            self.vx += nx * 0.05
            self.vy += ny * 0.05
        else:
            self.vx *= 0.85
            self.vy *= 0.85

        self.vx = max(-speed, min(self.vx, speed))
        self.vy = max(-speed, min(self.vy, speed))
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.9
        self.vy *= 0.9

        # Limite da tela
        jogo_ref.check_wall_collision(self) # <--- NOVO: Aplica colisão

        # --- ATAQUES ---

        # Ataque de chão: sempre disparado a cada cooldown
        if time.time() - getattr(self, "last_chao_time", 0) >= 1.5:  # cooldown chão
            self.atacar_chao(player)
            self.last_chao_time = time.time()

        # Ataque circular: somente se estiver próximo do jogador
        alcance_ataque_circular = 60
        if dist <= alcance_ataque_circular and time.time() - getattr(self, "last_especial_time", 0) >= self.ataque_especial_cooldown:
            self.ataques_chao.append(AtaqueCircular(
                boss=self,
                raio=30,
                duracao=0.5,
                dano=40,
                aviso_duracao=1.2
            ))
            self.last_especial_time = time.time()

        # Atualiza todos os ataques
        for ataque in self.ataques_chao[:]:
            ataque.update(player)
            if ataque.remover:
                self.ataques_chao.remove(ataque)

    def atacar_chao(self, player):
        largura = 20
        altura = 15
        self.ataques_chao.append(AtaqueChao(
            player.x - largura/2, player.y - altura/2,
            largura, altura,
            duracao=0.8,
            dano=40,
            aviso_duracao=0.5  # pisca 0.5s antes do dano
        ))
        self.last_especial_time = time.time()

        # Atualiza todos os ataques
        for ataque in self.ataques_chao[:]:
            ataque.update(player)
            if ataque.remover:
                self.ataques_chao.remove(ataque)

    def atacar_chao(self, player):
        largura = 20
        altura = 15
        self.ataques_chao.append(AtaqueChao(
            player.x - largura/2, player.y - altura/2,
            largura, altura,
            duracao=0.8,
            dano=40,
            aviso_duracao=0.5  # pisca 0.5s antes do dano
        ))

    def draw(self):
        cor_atual = 8 if hasattr(self, "dano_tempo") and time.time() < self.dano_tempo else self.cor
        
        # Desenha boss animado (maior que os outros)
        AnimationSystem.draw_boss_figure(
            self.x, self.y + self.raio, 
            cor_atual, self.animation_frame,
            1.5, self.is_moving
        )
        
        # Barra de vida
        barra_w, barra_h = 20, 3
        pyxel.rect(self.x - barra_w // 2, self.y - self.raio - 12, barra_w, barra_h, 7)
        pyxel.rect(self.x - barra_w // 2, self.y - self.raio - 12,
                  barra_w * self.vida / self.vida_max, barra_h, 8)

        # Desenha ataques
        for ataque in self.ataques_chao:
            ataque.draw()

class Bau:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = 4
        self.aberto = False
        self.item = None
        self.item_usado = False
        self.mostrar_msg = False
        self.msg = "F: Abrir bau"

    def draw(self, boss=None):
        if self.item_usado:
            return
        # O baú só deve aparecer e ser utilizável se o boss estiver morto ou ausente
        if boss is not None and boss.vida > 0:
            return
        
        x, y = self.x, self.y
        # Dimensões: 8 de largura, 6 de altura.
        w, h = 8, 6
        x_start = int(x - w // 2)
        y_start = int(y - h // 2)
        
        # --- 1. BASE DO BAÚ (Cor 9: Roxo Escuro) ---
        pyxel.rect(x_start, y_start + 1, w, h - 1, 9)
        # Detalhe/contorno preto
        pyxel.rectb(x_start, y_start + 1, w, h - 1, 0)
        
        if not self.aberto:
            # --- 2. BAÚ FECHADO ---
            # Tampa (Cor 10: Dourado)
            pyxel.rect(x_start, y_start, w, 2, 10)
            pyxel.rectb(x_start, y_start, w, 2, 0)
            # Fechadura (Cor 7: Branco)
            pyxel.rect(x - 1, y_start + 1, 2, 1, 7)
        else:
            # --- 3. BAÚ ABERTO ---
            
            # Tampa aberta e inclinada (deslocada para cima e para trás)
            pyxel.rect(x_start - 1, y_start - 3, w + 2, 2, 10) # Tampa
            pyxel.rectb(x_start - 1, y_start - 3, w + 2, 2, 0)

            # Brilho do Item (Glow)
            if self.item and not self.item_usado:
                
                # Mapeamento de cor do brilho
                if "Vida" in self.item:
                    glow_color = 11  # Azul Claro/Cura
                elif "Dano" in self.item:
                    glow_color = 8   # Vermelho/Ataque
                elif "Defesa" in self.item:
                    glow_color = 10  # Amarelo/Defesa
                else:
                    glow_color = 7 # Branco default
                    
                # Desenho do brilho animado/pulsante no centro da abertura
                # Brilho central maior
                pyxel.circ(x, y - 1, 2, glow_color)
                
                # Efeito de brilho piscando
                if pyxel.frame_count % 30 < 15:
                    pyxel.circb(x, y - 1, 3, glow_color)
                # Linhas decorativas (efeito de faísca)
                pyxel.line(x - 2, y - 3, x + 2, y + 1, glow_color)
                pyxel.line(x - 2, y + 1, x + 2, y - 3, glow_color)


        if self.mostrar_msg:
            # A mensagem é desenhada um pouco mais alto para evitar o baú
            pyxel.text(x - 20, y_start - 10, self.msg, 7)


class Altar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = 12
        self.mostrar_msg = False
        self.usado = False

    def draw(self, boss=None):
        if boss is not None and boss.vida > 0:
            return
        if self.mostrar_msg:
            pyxel.text(self.x - 23, self.y - 18, "F: usar altar", 7)


# --- MENU ---
class Menu:
    def __init__(self, jogo):
        self.jogo = jogo
        self.opcao = 0
        self.botao_largura = 69
        self.botao_altura = 20
        self.espaco = 5

        # lista de botões: [texto, x, y]
        self.botoes = [
            ["Jogar", 91.5, 55],
            ["Controles", 91.5, 80],
            ["Sair", 91.5, 104]
        ]
        self.aba_controles = False

    def update_menu(self):
        if self.aba_controles:
            if pyxel.btnp(pyxel.KEY_Q):
                self.aba_controles = False
                self.jogo.menu_ativo = True
            return

        # Navegação teclado
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.opcao = (self.opcao - 1) % len(self.botoes)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.opcao = (self.opcao + 1) % len(self.botoes)

        # Seleção teclado
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.acionar_botao(self.opcao)

        # Seleção mouse
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        for i, (_, x, y) in enumerate(self.botoes):
            if x <= mx <= x + self.botao_largura and y <= my <= y + self.botao_altura:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.acionar_botao(i)
                self.opcao = i  # destaque do mouse tem prioridade

    def acionar_botao(self, i):
        if i == 0:  # Jogar
            self.jogo.reset_jogo()   # <-- garante jogo novo
            self.jogo.menu_ativo = False
        elif i == 1:  # Controles
            self.aba_controles = True
        else:  # Sair
            pyxel.quit()

    def draw_menu(self):
        if self.aba_controles:
            pyxel.blt(0, 0, 1, 0, 0, 256, 144)

            # Fundo branco para o título "Controles:"
            titulo = "TAB: Pause"
            titulo_x = 5
            titulo_y = 20
            titulo_w = pyxel.width - 211  # cobre toda largura disponível
            titulo_h = 10
            pyxel.rect(titulo_x, titulo_y, titulo_w, titulo_h, 7)
            pyxel.text(titulo_x + 2, titulo_y + 1, titulo, 0)

            # Lista de controles
            controles = [
                "WASD/Setas: Mover",
                "SPACE/Mouse Esquerdo: Ataque",
                "SHIFT: Dash",
                "F: Interagir",
                "Q: Voltar pro menu"
            ]

            y_inicial = titulo_y + titulo_h + 5
            altura_caixa = 10
            espacamento = 5
            caixa_padding = 2  # padding interno

            for i, c in enumerate(controles):
                y = y_inicial + i * (altura_caixa + espacamento)
                texto_w = len(c) * 4 + caixa_padding * 2  # calcula largura do texto
                pyxel.rect(titulo_x, y, texto_w, altura_caixa, 7)  # fundo só atrás do texto
                pyxel.text(titulo_x + caixa_padding, y + 1, c, 0)
        else:
            pyxel.blt(0, 0, 0, 0, 0, 256, 144)
            for i, (texto, x, y) in enumerate(self.botoes):
                cor = 11 if self.opcao == i else 7
                pyxel.rect(x, y, self.botao_largura, self.botao_altura, cor)
                text_x = x + (self.botao_largura - len(texto) * 4) // 2
                text_y = y + (self.botao_altura - 8) // 2
                pyxel.text(text_x, text_y, texto, 0)


# --- JOGO ---
class Jogo:
    # --- COLISÃO ---
    WALL_LEFT = 12
    WALL_RIGHT = 243
    WALL_TOP = 21 # A barra superior no cenario.png
    WALL_BOTTOM = 118 # A barra inferior no cenario.png

    def __init__(self):
        pyxel.init(256, 144, title='Jogo', fps=60, quit_key=None)
        pyxel.image(0).load(0, 0, "menu.png")
        pyxel.image(1).load(0, 0, "controles.png")
        pyxel.image(2).load(0, 0, "cenario.png")
        
        self.menu_ativo = True
        self.menu = Menu(self)
        self.pausa_ativo = False
        self.game_over_ativo = False
        self.pause_opcao = 0
        self.game_over_opcao = 0
        self.altar_usos = 0
        self.inimigos_min = 3
        self.inimigos_max = 6

        # Paredes (Apenas para desenhar o cenario.png)
        self.lp = [] #(x, y, w, h, c)
        self.lp.append(Parede(0, 123, 256, 10, 10))  # Baixo
        self.lp.append(Parede(0, 0, 256, 20, 10))    # Cima
        self.lp.append(Parede(0, 0, 8, 144, 10))    # Esquerda
        self.lp.append(Parede(248, 0, 8, 144, 10))  # Direita

        # Altar Inicial
        self.altar = Altar(125, 72)

        # criação do personagem,boss, inimigos e baú
        x, y = self.get_posicao_aleatoria_personagem()
        self.p = Personagem(x, y, 5, 3, 100, 25, 0)
        self.boss = None
        self.li = []
        self.bau = None
        self.bau_cooldown = False

        self.co = self.colisao()
        pyxel.run(self.update, self.draw)

    # --- NOVO MÉTODO: Colisão com a Parede ---
    def check_wall_collision(self, entidade):
        """Força a entidade (Personagem, Inimigo, Boss) a permanecer dentro dos limites."""
        
        # Limite Esquerdo
        if entidade.x - entidade.raio < self.WALL_LEFT:
            entidade.x = self.WALL_LEFT + entidade.raio
            if hasattr(entidade, 'vx'):
                entidade.vx = 0
                
        # Limite Direito
        if entidade.x + entidade.raio > self.WALL_RIGHT:
            entidade.x = self.WALL_RIGHT - entidade.raio
            if hasattr(entidade, 'vx'):
                entidade.vx = 0
                
        # Limite Superior (A barra é desenhada a partir de y=0 e tem 20px de altura, mas a área de jogo começa em y=8)
        if entidade.y - entidade.raio < self.WALL_TOP:
            entidade.y = self.WALL_TOP + entidade.raio
            if hasattr(entidade, 'vy'):
                entidade.vy = 0
                
        # Limite Inferior (A barra é desenhada a partir de y=123 e tem 10px de altura)
        if entidade.y + entidade.raio > self.WALL_BOTTOM:
            entidade.y = self.WALL_BOTTOM - entidade.raio
            if hasattr(entidade, 'vy'):
                entidade.vy = 0

    # --- NOVO MÉTODO ---
    def get_posicao_aleatoria_personagem(self):
        while True:
            x = random.randint(self.WALL_LEFT + 5, self.WALL_RIGHT - 5)
            y = random.randint(self.WALL_TOP + 5, self.WALL_BOTTOM - 5)
            # Distância mínima do altar
            dist_altar = ((x - self.altar.x) ** 2 + (y - self.altar.y) ** 2) ** 0.5
            if dist_altar > self.altar.raio + 5:
                return x, y

    # --- RESET JOGO ---
    def reset_jogo(self):
        # Reset atributos do personagem
        self.p.vida_base = 100
        self.p.ataque_base = 25
        self.p.defesa_base = 11
        self.p.vida = self.p.vida_base
        self.p.ataque = self.p.ataque_base
        self.p.defesa = self.p.defesa_base

        # Resetar bônus
        self.p.bonus_vida = 0
        self.p.bonus_ataque = 0
        self.p.bonus_defesa = 0

        # Reset movimento e ataques
        self.p.vx = 0
        self.p.vy = 0
        self.p.attacking = False
        self.p.dashing = False
        self.p.targets_hit = set()
        self.p.is_moving = False

        # Reset estados de tela (CORRIGIDO: Não altera self.menu_ativo)
        self.pausa_ativa = False
        self.game_over_ativo = False

        # Reset altar / rounds
        self.altar_usos = 0
        self.altar = Altar(128, 72) # <-- Recria o altar na posição inicial

        # Reset inimigos e baús
        self.li.clear()
        self.boss = None # <-- Garante que o boss seja resetado
        self.bau = None
        self.bau_cooldown = False

        # Reset contadores de inimigos
        self.inimigos_min = 3
        self.inimigos_max = 6

        # Gera nova posição para o personagem
        x, y = self.get_posicao_aleatoria_personagem()
        self.p.x, self.p.y = x, y

    # --- UTIL ---
    def colisao(self):
        return {
            "cimaP": self.p.y - self.p.raio,
            "baixoP": self.p.y + self.p.raio,
            "direitaP": self.p.x + self.p.raio,
            "esquerdaP": self.p.x - self.p.raio
        }

    def get_attack_rect(self, atacante):
        rect_w, rect_h = 20, 3  # tamanho da espada
        dx, dy = atacante.last_dir_x, atacante.last_dir_y
        mag = (dx ** 2 + dy ** 2) ** 0.5 or 1
        nx, ny = dx / mag, dy / mag  # direção normalizada
        ortho_x, ortho_y = -ny, nx  # perpendicular

        # centro da espada
        cx = atacante.x + nx * rect_w / 2
        cy = atacante.y + ny * rect_w / 2

        # cantos do retângulo rotacionado
        p1 = (cx - nx * rect_w / 2 - ortho_x * rect_h / 2, cy - ny * rect_w / 2 - ortho_y * rect_h / 2)
        p2 = (cx + nx * rect_w / 2 - ortho_x * rect_h / 2, cy + ny * rect_w / 2 - ortho_y * rect_h / 2)
        p3 = (cx + nx * rect_w / 2 + ortho_x * rect_h / 2, cy + ny * rect_w / 2 + ortho_y * rect_h / 2)
        p4 = (cx - nx * rect_w / 2 + ortho_x * rect_h / 2, cy - ny * rect_w / 2 + ortho_y * rect_h / 2)

        # retorna bounding box (simplificada) para colisão
        xs = [p[0] for p in [p1, p2, p3, p4]]
        ys = [p[1] for p in [p1, p2, p3, p4]]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return [min_x, min_y, max_x - min_x, max_y - min_y]

    def draw_attack_visuals(self):
        if self.p.attacking:
            self.draw_attack_rotated(self.p, 8) # Cor não usada na nova função de espada
        for inimigo in self.li:
            if inimigo.attacking:
                self.draw_attack_rotated(inimigo, 13) # Cor não usada na nova função de espada

    def draw_attack_rotated(self, atacante, cor):
        """Desenha a espada com visual mais realista (cabo, guarda, lâmina)."""
        
        blade_length = 15  # Comprimento da lâmina
        handle_length = 5  # Comprimento do cabo
        blade_w = 2        # Largura da lâmina
        handle_w = 4       # Largura do cabo
        guard_w = 8        # Largura da guarda (no sentido ortogonal ao ataque)

        dx, dy = atacante.last_dir_x, atacante.last_dir_y
        mag = (dx ** 2 + dy ** 2) ** 0.5 or 1
        nx, ny = dx / mag, dy / mag  # direção normalizada
        ortho_x, ortho_y = -ny, nx  # vetor perpendicular (para a largura da espada)
        
        # Ponto de partida da espada (cruzamento do cabo/guarda, próximo ao corpo do atacante)
        start_x = atacante.x + nx * 5
        start_y = atacante.y + ny * 5
        
        # --- Desenhar Cabo (Handle) ---
        handle_end_x = start_x - nx * handle_length
        handle_end_y = start_y - ny * handle_length
        
        # Cabo: cor 0 (preto) - Usa linhas para simular um retângulo preenchido
        for i in range(-int(handle_w/2), int(handle_w/2) + 1):
             pyxel.line(start_x + i * ortho_x, start_y + i * ortho_y, 
                        handle_end_x + i * ortho_x, handle_end_y + i * ortho_y, 0)
        
        # --- Desenhar Guarda (Guard) ---
        guard_center_x = start_x - nx * 1 # Desloca ligeiramente na direção oposta ao ataque
        guard_center_y = start_y - ny * 1
        
        # Guarda: cor 7 (branco/cinza claro) - Desenha uma linha grossa
        for i in range(-int(guard_w/2), int(guard_w/2) + 1):
             pyxel.line(guard_center_x + i * ortho_x, guard_center_y + i * ortho_y, 
                        guard_center_x + i * ortho_x - nx * 1, guard_center_y + i * ortho_y - ny * 1, 7)


        # --- Desenhar Lâmina (Blade) ---
        blade_end_x = start_x + nx * blade_length
        blade_end_y = start_y + ny * blade_length
        
        # Lâmina: cor 7 (branco/cinza claro) - Usa linhas para simular um retângulo preenchido
        for i in range(-int(blade_w/2), int(blade_w/2) + 1):
             pyxel.line(start_x + i * ortho_x, start_y + i * ortho_y, 
                        blade_end_x + i * ortho_x, blade_end_y + i * ortho_y, 7)
                        
        # Adiciona a ponta da espada (triângulo)
        tip_x = blade_end_x + nx * 1
        tip_y = blade_end_y + ny * 1
        
        tip_base1_x = blade_end_x + ortho_x * blade_w / 2
        tip_base1_y = blade_end_y + ortho_y * blade_w / 2
        tip_base2_x = blade_end_x - ortho_x * blade_w / 2
        tip_base2_y = blade_end_y - ortho_y * blade_w / 2

        pyxel.tri(tip_x, tip_y, tip_base1_x, tip_base1_y, tip_base2_x, tip_base2_y, 7)
        
        # Linha central mais escura para detalhe
        pyxel.line(start_x, start_y, tip_x, tip_y, 14) 


    # --- ATAQUES ---
    def executar_ataque(self, atacante, alvos):
        if atacante.attacking and atacante.attack_frames > 0:
            attack_rect = self.get_attack_rect(atacante)
            for alvo in alvos:
                if alvo in atacante.targets_hit:
                    continue
                alvo_rect = [alvo.x - alvo.raio, alvo.y - alvo.raio, alvo.raio * 2, alvo.raio * 2]
                if (attack_rect[0] < alvo_rect[0] + alvo_rect[2] and
                        attack_rect[0] + attack_rect[2] > alvo_rect[0] and
                        attack_rect[1] < alvo_rect[1] + alvo_rect[3] and
                        attack_rect[1] + attack_rect[3] > alvo_rect[1]):
                    if getattr(alvo, 'dashing', False):
                        continue
                    
                    # Se o alvo é o Boss, passa self (o objeto Jogo) para o método tomar_dano
                    if isinstance(alvo, Boss):
                        alvo.tomar_dano(max(1, atacante.ataque - alvo.defesa), jogo=self)
                    else:
                        alvo.tomar_dano(max(1, atacante.ataque - alvo.defesa))
                        
                    dx, dy = alvo.x - atacante.x, alvo.y - atacante.y
                    mag = (dx ** 2 + dy ** 2) ** 0.5
                    if mag != 0:
                        # Colisão de repulsão:
                        repulse_factor = 1.5
                        alvo.vx += (dx / mag) * repulse_factor
                        alvo.vy += (dy / mag) * repulse_factor
                        
                        # Garante que o alvo não saia do mapa (importante após um empurrão forte)
                        self.check_wall_collision(alvo)
                        
                    atacante.targets_hit.add(alvo)
            atacante.attack_frames -= 1
        else:
            atacante.attacking = False

    def player_attack(self):
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)) and \
                (time.time() - self.p.last_attack_time >= 0.3):
            self.p.attacking = True
            self.p.attack_frames = 15
            self.p.last_attack_time = time.time()
            self.p.targets_hit = set()

    def process_attacks(self):
        alvos = self.li[:]
        if self.boss is not None and self.boss.vida > 0:
            alvos.append(self.boss)  # adiciona o boss como alvo
        self.executar_ataque(self.p, alvos)
        
        for inimigo in self.li:
            if time.time() < inimigo.stun_end_time:
                continue
            if not isinstance(inimigo, Arqueiro):
                dist = ((self.p.x - inimigo.x) ** 2 + (self.p.y - inimigo.y) ** 2) ** 0.5
                if dist < 20 and (time.time() - inimigo.last_attack_time >= 0.35):
                    inimigo.attacking = True
                    inimigo.attack_frames = 15
                    inimigo.last_attack_time = time.time()
                    inimigo.targets_hit = set()
                self.executar_ataque(inimigo, [self.p])

        # Também permite que boss ataque o player
        if self.boss is not None and self.boss.vida > 0:
            self.executar_ataque(self.boss, [self.p])

    # --- DASH ---
    def handle_dash(self):
        if pyxel.btnp(pyxel.KEY_SHIFT) and time.time() - self.p.last_dash_time >= self.p.dash_cooldown:
            self.p.dashing = True
            self.p.dash_frames = self.p.dash_duration
            self.p.last_dash_time = time.time()

        if self.p.dashing and self.p.dash_frames > 0:
            # Velocidade do Dash (movimentação própria, substitui dx/dy temporariamente)
            self.p.vx = self.p.last_dir_x * self.p.dash_speed
            self.p.vy = self.p.last_dir_y * self.p.dash_speed
            
            # Repulsão dos inimigos durante o dash
            for inimigo in self.li:
                dx, dy = inimigo.x - self.p.x, inimigo.y - self.p.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist < 10 and dist != 0:
                    push = 0.8
                    max_push_speed = 1.5
                    inimigo.vx += min((dx / dist) * push, max_push_speed)
                    inimigo.vy += min((dy / dist) * push, max_push_speed)
                    inimigo.stun_end_time = time.time() + 0.85
                    self.check_wall_collision(inimigo)
                    
            self.p.dash_frames -= 1
        else:
            self.p.dashing = False

    # --- COLISÕES ---
    def check_body_collisions(self):
        # Colisão Jogador vs Inimigos/Boss
        alvos = self.li[:]
        if self.boss is not None and self.boss.vida > 0:
            alvos.append(self.boss)
            
        for alvo in alvos:
            dx, dy = self.p.x - alvo.x, self.p.y - alvo.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            min_dist = self.p.raio + alvo.raio
            if dist < min_dist and dist > 0:
                overlap = min_dist - dist
                nx, ny = dx / dist, dy / dist
                # Divide o movimento de correção
                self.p.x += nx * (overlap / 2)
                self.p.y += ny * (overlap / 2)
                alvo.x -= nx * (overlap / 2)
                alvo.y -= ny * (overlap / 2)
                
                # Certifica que a correção não empurre para fora do limite
                self.check_wall_collision(self.p)
                self.check_wall_collision(alvo)

        # Colisão Inimigo vs Inimigo
        for i, inimigo in enumerate(self.li):
            for outro in self.li[i + 1:]:
                dx, dy = inimigo.x - outro.x, inimigo.y - outro.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                min_dist = inimigo.raio + outro.raio
                if dist < min_dist and dist > 0:
                    overlap = min_dist - dist
                    nx, ny = dx / dist, dy / dist
                    # Divide o movimento de correção
                    inimigo.x += nx * (overlap / 2)
                    inimigo.y += ny * (overlap / 2)
                    outro.x -= nx * (overlap / 2)
                    outro.y -= ny * (overlap / 2)
                    
                    # Certifica que a correção não empurre para fora do limite
                    self.check_wall_collision(inimigo)
                    self.check_wall_collision(outro)


    # --- UPDATE INIMIGOS ---
    def update_inimigos(self):
        # Se houver inimigos, atualizar normalmente
        for inimigo in self.li[:]:
            # Atualiza animação para todos os inimigos
            if hasattr(inimigo, 'update_animation'):
                inimigo.update_animation()
                
            if isinstance(inimigo, Arqueiro):
                # Passa a referência do objeto Jogo para o Arqueiro
                inimigo.update(self.p, self)
                
                # --- NOVO: checar colisão de projéteis com player ---
                for p in inimigo.projetis[:]:
                    dx, dy = self.p.x - p.x, self.p.y - p.y
                    dist = (dx**2 + dy**2)**0.5
                    if dist < self.p.raio + p.raio:  # colisão
                        self.p.tomar_dano(max(1, p.dano - self.p.defesa))
                        inimigo.projetis.remove(p)  # projétil some

                if inimigo.vida <= 0:
                    self.li.remove(inimigo)
                continue

            if time.time() < inimigo.stun_end_time:
                inimigo.x += inimigo.vx
                inimigo.y += inimigo.vy
                inimigo.vx *= 0.9
                inimigo.vy *= 0.9
                self.check_wall_collision(inimigo)
                continue

            dx = self.p.x - inimigo.x
            dy = self.p.y - inimigo.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            nx, ny = (dx / dist, dy / dist) if dist != 0 else (0, 0)

            if abs(nx) > abs(ny):
                inimigo.last_dir_x = int(nx / abs(nx)) if nx != 0 else 0
                inimigo.last_dir_y = 0
            else:
                inimigo.last_dir_x = 0
                inimigo.last_dir_y = int(ny / abs(ny)) if ny != 0 else 0

            follow_speed = 0.4
            acel = 0.1
            inimigo.vx += nx * acel
            inimigo.vy += ny * acel
            inimigo.vx = max(-follow_speed, min(inimigo.vx, follow_speed))
            inimigo.vy = max(-follow_speed, min(inimigo.vy, follow_speed))

            inimigo.x += inimigo.vx
            inimigo.y += inimigo.vy
            inimigo.vx *= 0.85  
            inimigo.vy *= 0.85

            self.check_wall_collision(inimigo)

            if inimigo.vida <= 0:
                self.li.remove(inimigo)

            # Se não houver inimigos vivos e altar já foi usado, criar baú
            if not self.li and self.altar and self.altar.usado and self.bau is None:
                self.bau = Bau(128, 20)
                self.bau.item = random.choice(["Vida +25%", "Dano +15%", "Defesa +15%"])
                self.bau.aberto = False
                self.bau.item_usado = False

    def update_pause(self):
        botoes_pause = ["Continuar", "Voltar ao menu"]
        largura, altura = 100, 20
        x = (pyxel.width - largura) // 2
        y_base = (pyxel.height - (len(botoes_pause) * (altura + 10))) // 2

        # --- Navegação teclado ---
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.pause_opcao = (self.pause_opcao - 1) % len(botoes_pause)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.pause_opcao = (self.pause_opcao + 1) % len(botoes_pause)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.acionar_pause(self.pause_opcao)

        # --- Navegação mouse ---
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        for i, _ in enumerate(botoes_pause):
            y = y_base + i * (altura + 10)
            if x <= mx <= x + largura and y <= my <= y + altura:
                self.pause_opcao = i  # destaque pelo mouse tem prioridade
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.acionar_pause(i)

    def acionar_pause(self, i):
        if i == 0:
            self.pausa_ativa = False  # continuar jogo
        else:
            self.pausa_ativa = True
            self.menu_ativo = True     # voltar ao menu

    # --- LÓGICA GAME OVER ---
    def acionar_game_over(self, i):
        if i == 0: # Jogar de Novo
            self.game_over_ativo = False
            self.reset_jogo() # Reseta o jogo
            self.menu_ativo = False # Garante que volte para a tela de jogo
        else: # Voltar ao menu
            self.game_over_ativo = False
            self.reset_jogo() # Reseta o jogo
            self.menu_ativo = True # CORRIGIDO: Garante que volte para o menu principal

    def update_game_over(self):
        botoes_game_over = ["Jogar de Novo", "Voltar ao menu"]
        largura, altura = 100, 20
        x = (pyxel.width - largura) // 2
        y_base = pyxel.height // 2 - 10 # Ponto de início para os botões

        # Navegação teclado
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.game_over_opcao = (self.game_over_opcao - 1) % len(botoes_game_over)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.game_over_opcao = (self.game_over_opcao + 1) % len(botoes_game_over)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.acionar_game_over(self.game_over_opcao)

        # Navegação mouse
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        for i, _ in enumerate(botoes_game_over):
            y = y_base + i * (altura + 10)
            if x <= mx <= x + largura and y <= my <= y + altura:
                self.game_over_opcao = i
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.acionar_game_over(i)


    # --- UPDATE ---
    def update(self):
        # Ativa o mouse se estiver no menu, pause ou game over
        pyxel.mouse((self.menu_ativo and not self.menu.aba_controles) or self.pausa_ativo or self.game_over_ativo)

        if self.menu_ativo:
            self.menu.update_menu()
            return

        # --- GAME OVER ---
        if self.p.vida <= 0 and not self.game_over_ativo:
            self.game_over_ativo = True
            self.game_over_opcao = 0 # Define a opção inicial
        
        if self.game_over_ativo:
            self.update_game_over()
            return # Pára o jogo e todo o resto do update

        # --- PAUSE ---
        if pyxel.btnp(pyxel.KEY_TAB) and not self.menu_ativo:
            self.pausa_ativa = not self.pausa_ativa

        if self.pausa_ativa:
            self.update_pause()
            return  # pára o resto do update enquanto estiver pausado

        # --- Lógica de Jogo Normal ---
        
        self.co = self.colisao()
        dir_x, dir_y = 0, 0

        #Movimentação do Jogador
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            self.p.y -= self.p.dy
            dir_y = -1
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.p.y += self.p.dy
            dir_y = 1
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.p.x += self.p.dx
            dir_x = 1
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            self.p.x -= self.p.dx
            dir_x = -1
            
        # Aplica colisão imediatamente após o movimento de base
        self.check_wall_collision(self.p)

        if dir_x != 0 or dir_y != 0:
            self.p.last_dir_x = dir_x
            self.p.last_dir_y = dir_y
        
        #Direção de ataque/dash
        if dir_x == 0 and dir_y == 0 and not self.p.dashing and (self.p.vx != 0 or self.p.vy != 0):
             mag = (self.p.vx ** 2 + self.p.vy ** 2) ** 0.5 or 1
             self.p.last_dir_x = self.p.vx / mag
             self.p.last_dir_y = self.p.vy / mag
        

        # Atualiza animação
        self.p.update_animation(dir_x, dir_y)

        self.handle_dash()
        self.player_attack()
        self.process_attacks()
        self.update_inimigos()

        # Aplica inércia (dash e repulsão)
        if self.p.dashing:
            self.p.x += self.p.vx
            self.p.y += self.p.vy
        
        self.p.vx *= 0.9
        self.p.vy *= 0.9
        self.p.x += self.p.vx # aplica a inércia restante
        self.p.y += self.p.vy
        
        # Aplica colisão após inércia
        self.check_wall_collision(self.p)

        self.check_body_collisions()

        # Atualiza o Boss se existir
        if self.boss is not None and self.boss.vida > 0:
            self.boss.update(self.p, self)
            self.executar_ataque(self.boss, [self.p])

            # Checa ataque corpo a corpo do Boss
            dx, dy = self.p.x - self.boss.x, self.p.y - self.boss.y
            dist = (dx**2 + dy**2)**0.5
            if dist < 15:  # alcance de ataque
                if time.time() - getattr(self.boss, 'last_attack_time', 0) >= 0.5:
                    self.boss.attacking = True
                    self.boss.attack_frames = 15
                    self.boss.last_attack_time = time.time()
                    self.boss.targets_hit = set()
            self.executar_ataque(self.boss, [self.p])


        # --- ALTAR ---
        if self.altar:
            # Só permite usar altar se não houver inimigos vivos E boss não estiver ativo
            boss_ativo = self.boss is not None and self.boss.vida > 0
            if not self.li and not boss_ativo:
                dx, dy = self.p.x - self.altar.x, self.p.y - self.altar.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist < self.p.raio + self.altar.raio:
                    self.altar.mostrar_msg = True
                    if pyxel.btnp(pyxel.KEY_F):
                        # Recupera vida do player
                        self.p.vida = min(self.p.vida_base, self.p.vida + int(self.p.vida_base * 0.5))
                        self.altar.usado = True
                        self.altar_usos += 1  # incrementa contador de usos/rounds

                        # Spawn do Boss a cada 5 usos
                        if self.altar_usos % 5 == 0:
                            if self.boss is None or self.boss.vida <= 0:
                                self.boss = Boss(128, 72)  # centro da tela
                            # não spawna inimigos normais neste round
                        else:
                            # Atualiza quantidade de inimigos baseados em rounds
                            if self.altar_usos % 3 == 0:
                                self.inimigos_min += 1
                                self.inimigos_max += 1

                            n_inimigos = random.randint(self.inimigos_min, self.inimigos_max)
                            n_arqueiros = int(n_inimigos * 0.3)
                            n_normais = n_inimigos - n_arqueiros

                            # Cria inimigos normais
                            for _ in range(n_normais):
                                while True:
                                    x = random.randint(20, 236)
                                    y = random.randint(20, 124)
                                    if ((x - self.p.x) ** 2 + (y - self.p.y) ** 2) ** 0.5 >= 40:
                                        break
                                inimigo = Inimigo(x, y)
                                escala = 1 + self.altar_usos * 0.15  # aumenta stats por round
                                inimigo.vida = int(inimigo.vida * escala)
                                inimigo.vida_max = inimigo.vida
                                self.li.append(inimigo)

                            # Cria arqueiros
                            for _ in range(n_arqueiros):
                                while True:
                                    x = random.randint(20, 236)
                                    y = random.randint(20, 124)
                                    if ((x - self.p.x) ** 2 + (y - self.p.y) ** 2) ** 0.5 >= 40:
                                        break
                                arqu = Arqueiro(x, y)
                                escala = 1 + self.altar_usos * 0.15
                                arqu.vida = int(arqu.vida * escala)
                                arqu.vida_max = arqu.vida
                                self.li.append(arqu)

                        self.bau = Bau(127, 23)
                        self.bau.item = random.choice(["Vida +25%", "Dano +15%", "Defesa +15%"])
                else:
                    self.altar.mostrar_msg = False

        # --- BAÚ ---
        if self.bau and not self.li:
            dx, dy = self.p.x - self.bau.x, self.p.y - self.bau.y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            # Colisão física (impede atravessar o baú)
            min_dist = self.p.raio + self.bau.raio
            if dist < min_dist and dist > 0:
                overlap = min_dist - dist
                nx, ny = dx / dist, dy / dist
                self.p.x += nx * overlap
                self.p.y += ny * overlap
                # Garante que a colisão com o baú não empurre o player para fora do mapa
                self.check_wall_collision(self.p)

            # Interação com F (mostra mensagem e permite pegar item)
            alcance = self.p.raio + self.bau.raio + 7  # distância maior para mostrar a mensagem
            if dist < alcance:
                self.bau.mostrar_msg = True
                if pyxel.btnp(pyxel.KEY_F) and not self.bau_cooldown:
                    if not self.bau.aberto:
                        self.bau.aberto = True
                        self.bau.item_usado = False
                        self.bau.msg = f"{self.bau.item}"
                    elif not self.bau.item_usado:
                        if self.bau.item == "Vida +25%":
                            self.p.bonus_vida += 0.25
                            # Aumenta apenas a vida máxima, sem alterar a vida atual
                            self.p.vida_base = int(100 * (1 + self.p.bonus_vida))
                        elif self.bau.item == "Dano +15%":
                            self.p.bonus_ataque += 0.15
                            self.p.ataque_base = int(25 * (1 + self.p.bonus_ataque))
                            self.p.ataque = self.p.ataque_base
                        elif self.bau.item == "Defesa +15%":
                            self.p.bonus_defesa += 0.15
                            self.p.defesa_base = int(11 * (1 + self.p.bonus_defesa))
                            self.p.defesa = self.p.defesa_base

                        # Limitar bônus máximos
                        self.p.bonus_vida = min(self.p.bonus_vida, 3)      # +300% máximo
                        self.bau.item_usado = True
            else:
                self.bau.mostrar_msg = False

   # --- DRAW ROUND PANEL (UI bonitinha) ---
    def draw_round_panel(self):
        pad = 1.45          # espaçamento da borda da tela
        w = 50           # largura do painel
        h = 15           # altura do painel
        x = pyxel.width - w - pad  # canto direito da tela
        y = pad                    # canto superior da tela

        # Sombra
        pyxel.rect(x + 1, y + 1, w, h, 0)

        # Fundo do painel
        pyxel.rect(x, y, w, h // 2, 12)  # faixa superior
        pyxel.rect(x, y + h // 2, w, h - h // 2, 6)  # faixa inferior

        # Borda
        pyxel.rectb(x - 1, y - 1, w + 2, h + 2, 7)

        # Label
        label = "ROUND"
        pyxel.text(x + 2, y + 1, label, 7)

        # Número centralizado à direita dentro do painel
        num = str(self.altar_usos)
        cor_num = 10 if (self.altar_usos % 2 == 0) else 11
        num_w = len(num) * 4  # cada caractere tem ~4 pixels de largura
        num_x = x + w - num_w - 2  # colado na borda direita com 2px de padding
        num_y = y + (h - 8) // 2   # centralizado verticalmente (altura do texto = 8px)
        pyxel.text(num_x - 1, num_y - 1, num, 0)  # sombra
        pyxel.text(num_x, num_y, num, cor_num)

        # Detalhes decorativos
        pyxel.pset(x + 3, y + h - 4, 11)
        pyxel.pset(x + 6, y + h - 6, 13)
        pyxel.pset(x + w - 6, y + 3, 14)

    # --- DRAW GAME OVER ---
    def draw_game_over(self):
        # Fundo semi-transparente estilo "vidro fosco" (igual ao pause)
        for yy in range(pyxel.height):
            for xx in range(pyxel.width):
                if (xx + yy) % 4 == 0:
                    pyxel.pset(xx, yy, 0)
                elif (xx + yy) % 4 == 1:
                    pyxel.pset(xx, yy, 7)
        
        # Título "GAME OVER" (MODIFICADO: Maior e Branco com outline preto)
        titulo = "G A M E   O V E R" # Espaços extras para efeito de texto grande
        titulo_w = len(titulo) * 4 # A largura é baseada no número de caracteres (4px/char)
        titulo_x = (pyxel.width - titulo_w) // 2
        titulo_y = pyxel.height // 2 - 40
        
        # Desenha a borda/sombra (preta, cor 0)
        pyxel.text(titulo_x - 1, titulo_y, titulo, 0)
        pyxel.text(titulo_x + 1, titulo_y, titulo, 0)
        pyxel.text(titulo_x, titulo_y - 1, titulo, 0)
        pyxel.text(titulo_x, titulo_y + 1, titulo, 0)
        
        # Desenha o texto principal (branco, cor 7)
        pyxel.text(titulo_x, titulo_y, titulo, 8)
        
        # Botões centralizados
        botoes_game_over = ["Jogar de Novo", "Voltar ao menu"]
        largura, altura = 100, 20
        x = (pyxel.width - largura) // 2
        y_base = pyxel.height // 2 - 10
        
        for i, texto in enumerate(botoes_game_over):
            y = y_base + i * (altura + 10)
            cor = 8 if self.game_over_opcao == i else 7 # Vermelho para destaque
            pyxel.rect(x, y, largura, altura, cor)
            pyxel.text(x + (largura - len(texto) * 4) // 2, y + 6, texto, 0) # Texto preto

    # --- DRAW (MODIFICADO) ---
    def draw(self):
        if self.menu_ativo:
            self.menu.draw_menu()
            return

        pyxel.cls(0)
        for parede in self.lp:
            parede.draw()
        for inimigo in self.li:
            inimigo.draw()
        if self.boss is not None and self.boss.vida > 0:
            self.boss.draw()


        self.p.draw()
        self.draw_attack_visuals()

        if self.bau and not self.li:
            self.bau.draw(boss=self.boss)
        if self.altar and not self.li:
            self.altar.draw(boss=self.boss)

        # HUD do jogador
        max_barra = 40  # largura da barra base para vida 100
        barra_jogador_w = max_barra * (self.p.vida_base / 100)  # aumenta proporcionalmente à vida máxima
        barra_jogador_h = 3
        # Fundo da barra (vida máxima)
        pyxel.rect(2, 2, barra_jogador_w, barra_jogador_h, 7)
        # Vida atual proporcional à vida máxima
        vida_ratio = min(1, self.p.vida / self.p.vida_base)
        pyxel.rect(2, 2, barra_jogador_w * vida_ratio, barra_jogador_h, 11)

        cooldown = max(0, min(1, (time.time() - self.p.last_dash_time) / self.p.dash_cooldown))
        barra_largura = 30
        pyxel.rect(2, 6, barra_largura, 2, 7)
        pyxel.rect(2, 6, barra_largura * cooldown, 2, 8)

        # --- Round panel (bonitinho) ---
        self.draw_round_panel()
        
        # --- DRAW GAME OVER OVERLAY (PRIORIDADE MÁXIMA) ---
        if self.game_over_ativo:
            self.draw_game_over()
            return # Pára de desenhar o resto (incluindo pause)

        # --- DRAW PAUSE OVERLAY ---
        if self.pausa_ativa:
            # Fundo semi-transparente estilo "vidro fosco" com cores escuras
            for yy in range(pyxel.height):
                for xx in range(pyxel.width):
                    if (xx + yy) % 4 == 0:
                        pyxel.pset(xx, yy, 0)  # preto mais forte
                    elif (xx + yy) % 4 == 1:
                        pyxel.pset(xx, yy, 7)  # cinza escuro

             # Título "P A U S E" 
            titulo = "P A U S E" # Espaços extras para efeito de texto grande
            titulo_w = len(titulo) * 4 # A largura é baseada no número de caracteres (4px/char)
            titulo_x = (pyxel.width - titulo_w) // 2
            titulo_y = pyxel.height // 2 - 40
            
            # Desenha a borda/sombra (preta, cor 0)
            pyxel.text(titulo_x - 1, titulo_y, titulo, 0)
            pyxel.text(titulo_x + 1, titulo_y, titulo, 0)
            pyxel.text(titulo_x, titulo_y - 1, titulo, 0)
            pyxel.text(titulo_x, titulo_y + 1, titulo, 0)
        
            # Desenha o texto principal (branco, cor 7)
            pyxel.text(titulo_x, titulo_y, titulo, 7)

            # Botões centralizados
            botoes_pause = ["Continuar", "Voltar ao menu"]
            largura, altura = 100, 20
            x = (pyxel.width - largura) // 2
            y_base = (pyxel.height - (len(botoes_pause) * (altura + 10))) // 2

            for i, texto in enumerate(botoes_pause):
                y = y_base + i * (altura + 10)
                cor = 11 if self.pause_opcao == i else 7
                pyxel.rect(x, y, largura, altura, cor)
                pyxel.text(x + (largura - len(texto) * 4) // 2, y + 6, texto, 0)
            return

Jogo()