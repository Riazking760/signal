import logging
import random
import pygame
import numpy as np
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেট আপ করা
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Pygame ইনিশিয়ালাইজ করা
pygame.init()

# স্ক্রীন সেট আপ
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('3D Wheel')

# রঙ সংজ্ঞায়িত করা
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# চাকা এর ভেরিয়েবল
wheel_radius = 200
wheel_center = (400, 300)

# চাকার জন্য অপশন
options = ['🍏', '🍎', '🍌', '🍇', '🍊', '🍗', '🍕', '🍔', '🍣', '🍩']

# চাকা ঘোরানোর ফাংশন
def draw_wheel(angle):
    screen.fill(WHITE)
    for i, option in enumerate(options):
        # কোণ তৈরি করা
        theta = angle + (i * (360 / len(options))) * np.pi / 180
        x = wheel_center[0] + wheel_radius * np.cos(theta)
        y = wheel_center[1] + wheel_radius * np.sin(theta)
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 20)
        font = pygame.font.Font(None, 36)
        text = font.render(option, True, BLACK)
        screen.blit(text, (x - 10, y - 10))
    pygame.display.flip()

# টেলিগ্রাম বট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('বেটিং গেমে স্বাগতম! খেলা শুরু করতে /play লিখুন।')

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("চাকা ঘুরাতে শুরু করা হচ্ছে...")
    
    # Pygame এ চাকা ঘোরানোর মেইন লুপ
    running = True
    angle = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        angle += random.randint(1, 5)  # চাকা ঘুরানো
        draw_wheel(np.radians(angle))  # চাকা আঁকা

        pygame.time.delay(100)
    
    # পুরস্কার নির্বাচন করা
    prize = random.choice(options)
    await update.message.reply_text(f'আপনি {prize} এর সাথে জিতেছেন!')

def main():
    # টেলিগ্রাম বটের অ্যাপ্লিকেশন তৈরি করা
    application = ApplicationBuilder().token('7527810081:AAEOK4wUYj2OKpCZQldcQHgULAy4JZRtRss').build()

    # হ্যান্ডলার যুক্ত করা
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('play', play))

    # বট শুরু করা
    try:
        application.run_polling()
    except Exception as e:
        logging.error(f"বট চালানোর সময় একটি ত্রুটি ঘটেছে: {e}")

if __name__ == '__main__':
    main()
