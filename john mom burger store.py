import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("John's Mom Burger Store - Build Your Own!")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
GREEN = (80, 200, 80)
YELLOW = (255, 220, 100)
BLUE = (100, 150, 255)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (210, 180, 140)
DARK_BROWN = (101, 67, 33)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
PINK = (255, 180, 180)
GOLD = (255, 215, 0)
TOMATO_RED = (255, 99, 71)
LETTUCE_GREEN = (50, 205, 50)
CHEESE_YELLOW = (255, 223, 0)

# Fonts
font_small = pygame.font.Font(None, 20)
font_mid = pygame.font.Font(None, 26)
font_big = pygame.font.Font(None, 36)
font_huge = pygame.font.Font(None, 48)


# Game state
class GameState:
    def __init__(self):
        self.money = 500
        self.reputation = 50
        self.day = 1
        self.customers_served = 0
        self.customers_today_limit = random.randint(5, 8)
        self.inventory = {
            "Bun": 30,
            "Patty": 25,
            "Lettuce": 20,
            "Cheese": 15,
            "Tomato": 15,
            "Onion": 10
        }
        self.current_customer = None
        self.customer_queue = []
        self.building_burger = []
        self.burger_complete = False
        self.message = ""
        self.message_timer = 0
        self.game_over = False
        self.day_ended = False


# Burger recipes (what customers want)
recipes = {
    "Classic": ["Bun", "Patty", "Lettuce", "Bun"],
    "Cheeseburger": ["Bun", "Patty", "Cheese", "Lettuce", "Bun"],
    "Double": ["Bun", "Patty", "Cheese", "Patty", "Lettuce", "Bun"],
    "Deluxe": ["Bun", "Patty", "Cheese", "Tomato", "Lettuce", "Onion", "Bun"],
    "Veggie": ["Bun", "Lettuce", "Tomato", "Onion", "Lettuce", "Bun"]
}

recipe_prices = {
    "Classic": 15,
    "Cheeseburger": 20,
    "Double": 28,
    "Deluxe": 35,
    "Veggie": 18
}

# Customer types
customer_types = [
    {"name": "Regular", "patience": 60, "color": BLUE},
    {"name": "Hungry", "patience": 45, "color": ORANGE},
    {"name": "Foodie", "patience": 75, "color": PINK}
]


class Customer:
    def __init__(self, index):
        ctype = random.choice(customer_types)
        self.name = ctype["name"]
        self.max_patience = ctype["patience"]
        self.patience = self.max_patience
        self.color = ctype["color"]
        self.order_name = random.choice(list(recipes.keys()))
        self.order = recipes[self.order_name].copy()
        self.x = 120 + (index * 100)
        self.y = 120
        self.arrived = False

    def update(self):
        if not self.arrived:
            self.arrived = True
        self.patience -= 1 / 60

    def draw(self, screen, is_current=False):
        # Draw customer body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 28)
        # Draw face
        pygame.draw.circle(screen, WHITE, (int(self.x) - 10, int(self.y) - 6), 5)
        pygame.draw.circle(screen, WHITE, (int(self.x) + 10, int(self.y) - 6), 5)
        pygame.draw.circle(screen, BLACK, (int(self.x) - 10, int(self.y) - 6), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 10, int(self.y) - 6), 2)

        # Draw mouth
        if self.patience < self.max_patience * 0.3:
            # Sad mouth
            pygame.draw.arc(screen, BLACK, (int(self.x) - 12, int(self.y) + 4, 24, 16), 3.14, 0, 2)
        else:
            # Happy mouth
            pygame.draw.arc(screen, BLACK, (int(self.x) - 12, int(self.y), 24, 16), 0, 3.14, 2)

        # Highlight current customer
        if is_current:
            pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), 33, 3)

        # Draw patience bar
        bar_width = 56
        bar_height = 6
        patience_ratio = max(0, self.patience / self.max_patience)
        pygame.draw.rect(screen, DARK_GRAY, (self.x - bar_width // 2, self.y + 36, bar_width, bar_height))
        color = GREEN if patience_ratio > 0.5 else ORANGE if patience_ratio > 0.25 else RED
        pygame.draw.rect(screen, color, (self.x - bar_width // 2, self.y + 36, bar_width * patience_ratio, bar_height))

        # Draw order name
        draw_text_centered(f"{self.order_name}", int(self.x), self.y + 52, font_small, BLACK)


class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.enabled = True

    def draw(self, screen):
        if not self.enabled:
            current_color = DARK_GRAY
        else:
            mouse_pos = pygame.mouse.get_pos()
            current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text_surf = font_mid.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self):
        return self.enabled and self.rect.collidepoint(pygame.mouse.get_pos())


def draw_text(text, x, y, color=BLACK, font_type=font_mid):
    text_surf = font_type.render(text, True, color)
    screen.blit(text_surf, (x, y))


def draw_text_centered(text, x, y, font_type=font_mid, color=BLACK):
    text_surf = font_type.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)


def check_ingredients(item):
    return game_state.inventory.get(item, 0) > 0


def use_ingredient(item):
    if item in game_state.inventory:
        game_state.inventory[item] -= 1


def add_layer(layer):
    if check_ingredients(layer):
        use_ingredient(layer)
        game_state.building_burger.append(layer)
        check_burger_complete()
        return True
    return False


def check_burger_complete():
    if not game_state.current_customer:
        return

    built = game_state.building_burger
    wanted = game_state.current_customer.order

    if len(built) == len(wanted) and built == wanted:
        game_state.burger_complete = True
        show_message("Burger Complete! Ready to serve!")


def serve_customer():
    if not game_state.burger_complete or not game_state.current_customer:
        return

    bonus = 0
    if game_state.current_customer.patience > game_state.current_customer.max_patience * 0.5:
        bonus = 5

    earnings = recipe_prices[game_state.current_customer.order_name] + bonus
    game_state.money += earnings
    game_state.reputation += 2
    game_state.customers_served += 1

    if bonus > 0:
        show_message(f"Served! +${earnings} (Fast bonus: +${bonus})")
    else:
        show_message(f"Served! +${earnings}")

    # Remove current customer, next customer moves forward
    game_state.customer_queue.pop(0)
    game_state.current_customer = None
    game_state.building_burger = []
    game_state.burger_complete = False

    # If there's next customer, set as current
    if game_state.customer_queue:
        game_state.current_customer = game_state.customer_queue[0]


def show_message(msg, duration=2000):
    game_state.message = msg
    game_state.message_timer = pygame.time.get_ticks()


def buy_ingredients():
    cost = 50
    if game_state.money >= cost:
        game_state.money -= cost
        for item in game_state.inventory:
            game_state.inventory[item] += 5
        show_message("Ingredients purchased!")


def next_day():
    game_state.day += 1
    game_state.customers_served = 0
    game_state.customers_today_limit = random.randint(5, 8)
    game_state.current_customer = None
    game_state.customer_queue = []
    game_state.building_burger = []
    game_state.burger_complete = False
    generate_customers()
    show_message(f"Day {game_state.day} started!")


def generate_customers():
    game_state.customer_queue = []
    for i in range(game_state.customers_today_limit):
        customer = Customer(i)
        game_state.customer_queue.append(customer)
    if game_state.customer_queue:
        game_state.current_customer = game_state.customer_queue[0]


def draw_burger_layer(screen, layer, index, total_layers, x, y_start):
    """Draw each layer of the burger"""
    layer_height = 20
    y_offset = y_start - (total_layers * layer_height // 2) + (index * layer_height)

    if layer == "Bun":
        # Check if top or bottom bun
        if index == 0:  # Top bun
            pygame.draw.ellipse(screen, LIGHT_BROWN, (x - 50, y_offset, 100, 33))
            pygame.draw.ellipse(screen, BROWN, (x - 50, y_offset, 100, 33), 2)
            # Sesame seeds
            for i in range(4):
                pygame.draw.circle(screen, YELLOW, (x - 33 + i * 22, y_offset + 8), 2)
        else:  # Bottom bun
            pygame.draw.ellipse(screen, LIGHT_BROWN, (x - 50, y_offset, 100, 28))
            pygame.draw.ellipse(screen, BROWN, (x - 50, y_offset, 100, 28), 2)
    elif layer == "Patty":
        pygame.draw.ellipse(screen, DARK_BROWN, (x - 48, y_offset + 4, 96, 25))
        pygame.draw.ellipse(screen, BROWN, (x - 48, y_offset + 4, 96, 25), 2)
    elif layer == "Cheese":
        pygame.draw.polygon(screen, CHEESE_YELLOW, [
            (x - 54, y_offset + 8),
            (x + 54, y_offset + 8),
            (x + 50, y_offset + 20),
            (x - 50, y_offset + 20)
        ])
        pygame.draw.polygon(screen, GOLD, [
            (x - 54, y_offset + 8),
            (x + 54, y_offset + 8),
            (x + 50, y_offset + 20),
            (x - 50, y_offset + 20)
        ], 2)
    elif layer == "Lettuce":
        pygame.draw.ellipse(screen, LETTUCE_GREEN, (x - 52, y_offset + 4, 104, 20))
        pygame.draw.ellipse(screen, GREEN, (x - 52, y_offset + 4, 104, 20), 2)
    elif layer == "Tomato":
        pygame.draw.ellipse(screen, TOMATO_RED, (x - 46, y_offset + 6, 92, 18))
        pygame.draw.ellipse(screen, RED, (x - 46, y_offset + 6, 92, 18), 2)
    elif layer == "Onion":
        pygame.draw.ellipse(screen, (200, 200, 255), (x - 42, y_offset + 6, 84, 16))
        pygame.draw.ellipse(screen, (150, 150, 200), (x - 42, y_offset + 6, 84, 16), 2)


# Create buttons
btn_bun = Button(30, 80, 100, 38, "Bun", LIGHT_BROWN, BROWN)
btn_patty = Button(30, 125, 100, 38, "Patty", DARK_BROWN, BROWN)
btn_lettuce = Button(30, 170, 100, 38, "Lettuce", LETTUCE_GREEN, GREEN)
btn_cheese = Button(30, 215, 100, 38, "Cheese", CHEESE_YELLOW, GOLD)
btn_tomato = Button(30, 260, 100, 38, "Tomato", TOMATO_RED, RED)
btn_onion = Button(30, 305, 100, 38, "Onion", (200, 200, 255), (150, 150, 200))
btn_clear = Button(30, 360, 100, 42, "Clear", RED, (255, 100, 100))
btn_serve = Button(30, 415, 100, 42, "Serve", ORANGE, (255, 200, 0))
btn_buy = Button(820, 560, 140, 45, "Buy Stock $50", BLUE, (150, 200, 255))
btn_next_day = Button(30, 560, 120, 45, "Next Day", BROWN, (180, 100, 50))

# Initialize game state
game_state = GameState()
generate_customers()

# Main loop
running = True
while running:
    screen.fill(WHITE)
    dt = clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_bun.is_clicked() and game_state.current_customer and not game_state.burger_complete:
                add_layer("Bun")
            if btn_patty.is_clicked() and game_state.current_customer and not game_state.burger_complete:
                add_layer("Patty")
            if btn_lettuce.is_clicked() and game_state.current_customer and not game_state.burger_complete:
                add_layer("Lettuce")
            if btn_cheese.is_clicked() and game_state.current_customer and not game_state.burger_complete:
                add_layer("Cheese")
            if btn_tomato.is_clicked() and game_state.current_customer and not game_state.burger_complete:
                add_layer("Tomato")
            if btn_onion.is_clicked() and game_state.current_customer and not game_state.burger_complete:
                add_layer("Onion")

            if btn_clear.is_clicked():
                game_state.building_burger = []
                game_state.burger_complete = False
                show_message("Cleared")

            if btn_serve.is_clicked() and game_state.burger_complete:
                serve_customer()

            if btn_buy.is_clicked():
                buy_ingredients()

            if btn_next_day.is_clicked():
                next_day()

    # Update customer
    if game_state.current_customer:
        game_state.current_customer.update()
        if game_state.current_customer.patience <= 0:
            show_message("Customer left angry!")
            game_state.reputation -= 5
            game_state.customer_queue.pop(0)
            game_state.current_customer = None
            game_state.building_burger = []
            game_state.burger_complete = False
            if game_state.customer_queue:
                game_state.current_customer = game_state.customer_queue[0]

    # Draw UI
    draw_text("John's Mom Burger Store", 280, 10, color=BROWN, font_type=font_huge)
    draw_text(f"Day: {game_state.day}", 320, 55, font_type=font_mid)
    draw_text(f"Money: ${game_state.money}", 500, 55, font_type=font_mid)
    draw_text(f"Reputation: {game_state.reputation}", 680, 55, font_type=font_mid)
    draw_text(f"Served: {game_state.customers_served}/{game_state.customers_today_limit}", 320, 80,
              font_type=font_small)

    # Draw inventory
    draw_text("Inventory:", 820, 85, font_type=font_mid)
    y = 110
    for item, count in game_state.inventory.items():
        color = RED if count < 5 else BLACK
        draw_text(f"{item}: {count}", 820, y, font_type=font_small, color=color)
        y += 22

    # Draw ingredient buttons
    btn_bun.draw(screen)
    btn_patty.draw(screen)
    btn_lettuce.draw(screen)
    btn_cheese.draw(screen)
    btn_tomato.draw(screen)
    btn_onion.draw(screen)
    btn_clear.draw(screen)
    btn_serve.draw(screen)
    btn_buy.draw(screen)
    btn_next_day.draw(screen)

    # Draw customer queue
    if game_state.customer_queue:
        draw_text_centered("Customer Queue", WIDTH // 2, 40, font_big, BROWN)
        for i, customer in enumerate(game_state.customer_queue[:7]):
            is_current = (i == 0)
            customer.x = 120 + (i * 100)
            customer.draw(screen, is_current)
    else:
        draw_text_centered("No more customers today", WIDTH // 2, 120, font_big, DARK_GRAY)

    # Draw building burger
    if game_state.building_burger:
        center_x = WIDTH // 2
        center_y = 430
        draw_text_centered("Building Burger", center_x, 300, font_big, ORANGE)
        for i, layer in enumerate(game_state.building_burger):
            draw_burger_layer(screen, layer, i, len(game_state.building_burger), center_x, center_y)

    # Show target recipe
    if game_state.current_customer:
        draw_text_centered(f"Wants: {game_state.current_customer.order_name}", WIDTH // 2, 210, font_big, BLUE)
        draw_text_centered(f"Recipe: {' -> '.join(game_state.current_customer.order)}", WIDTH // 2, 240, font_small,
                           DARK_GRAY)

    # If burger complete, highlight
    if game_state.burger_complete:
        draw_text_centered("✓ Burger Complete!", WIDTH // 2, 560, font_big, GREEN)

    # Show message
    if game_state.message:
        now = pygame.time.get_ticks()
        if now - game_state.message_timer < 2000:
            draw_text_centered(game_state.message, WIDTH // 2, 40, font_big, RED)
        else:
            game_state.message = ""

    # Instructions
    draw_text_centered("Click to add ingredients | Follow recipe | Serve when done", WIDTH // 2, 630, font_small,
                       DARK_GRAY)

    pygame.display.flip()

pygame.quit()
sys.exit()
