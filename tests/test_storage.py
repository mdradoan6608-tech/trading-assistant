from storage.watchlist import get_watchlist, save_watchlist

symbols = get_watchlist()

print(symbols)

symbols.append("VOO")

save_watchlist(symbols)

print(get_watchlist())
