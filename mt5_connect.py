import MetaTrader5 as mt5

# Hisob ma'lumotlari
login = 313652330
password = "Azamat2301,"
server = "XMGlobal-MT5 7"

# Terminalga ulanish
if not mt5.initialize():
    print("❌ MT5 initialize xatolik:", mt5.last_error())
    quit()

# Login qilish
authorized = mt5.login(login, password=password, server=server)
if not authorized:
    print("❌ Login xatolik:", mt5.last_error())
    mt5.shutdown()
    quit()

# Hisob ma'lumotlarini chiqarish
account_info = mt5.account_info()
if account_info is None:
    print("Hisob ma'lumotlari olinmadi")
else:
    print(f"✅ Ulandi: Login: {account_info.login}, Balance: {account_info.balance}, Equity: {account_info.equity}")

mt5.shutdown()
