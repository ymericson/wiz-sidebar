from nba_data import perGame, schedule, standings
import tabulate

def df_to_markdown(*dfs, sep_line='\n---\n', **kwargs):
    disable_numparse = kwargs.pop('disable_numparse', True)
    tablefmt = kwargs.pop('tablefmt', 'pipe')
    headers = kwargs.pop('headers', 'keys')
    
    for df in dfs:
        print(tabulate.tabulate(df,
                                tablefmt = tablefmt,
                                headers = headers,
                                disable_numparse = disable_numparse,
                                **kwargs))
        if sep_line is not None:
            print(sep_line)

print(perGame)
print()
print(schedule)
print()
print(standings)
# a, b, c = nba-data.main()
# print(a)