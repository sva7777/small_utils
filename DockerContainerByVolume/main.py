import io
import subprocess
import pandas as pd


def show_container_for_volumes():
    results = subprocess.run('docker volume ls', capture_output=True, text=True,  shell=True)

    df = pd.read_csv(io.StringIO(results.stdout),
                     encoding='utf8',
                     sep="    ",
                     engine='python')

    for i, row in df.iterrows():
        print(i, row['VOLUME NAME'])
        print('-' * 20)
        cmd = ['docker', 'ps', '-a', '--filter', f'volume={row["VOLUME NAME"]}']
        print(subprocess.run(cmd,
               capture_output=True, text=True).stdout)
        print()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    show_container_for_volumes()


