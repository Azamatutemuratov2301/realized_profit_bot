from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Realized Profit Bot is running"}
# main.py
from bot import TradingBot

def main():
    bot = TradingBot()
    
    while True:
        bot.show_menu()
        choice = input(bot.get_text('enter_choice') + ": ")
        
        if choice == '1':
            # Foyda hisoblash
            try:
                entry = float(input(bot.get_text('enter_entry_price')))
                exit = float(input(bot.get_text('enter_exit_price')))
                qty = float(input(bot.get_text('enter_quantity')))
                print(bot.calculate_profit(entry, exit, qty))
            except ValueError:
                print(bot.get_text('invalid_input'))
        
        elif choice == '2':
            # Tilni o'zgartirish
            print("\n".join([
                f"{i+1}. {LANGUAGES[lang]['language_name']}" 
                for i, lang in enumerate(LANGUAGES)
            ]))
            lang_choice = input(bot.get_text('choose_language') + ": ")
            print(bot.set_language(list(LANGUAGES.keys())[int(lang_choice)-1]))
        
        elif choice == '3':
            print(bot.get_text('goodbye'))
            break

if name == "main":
    main()
