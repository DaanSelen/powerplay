import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class process():
    @staticmethod
    def convert(nid_rows):
        df = pd.DataFrame([
            {
                'timestamp': time,
                'nodeid': data['nodeid'],
                'power': data['power'],
                'oldpower': data['oldPower'] if "oldPower" in data else "Absent"
            }
            for time, data in nid_rows
        ])

        return df
    
    def insert_name(df, name):
        df['nodename'] = name
        return df

    def stitch_plot(node_dfs: dict):
        """
        node_dfs: dict of {nodeid: dataframe}
        Returns a single stitched plot with one row per node
        """
        num_nodes = len(node_dfs)
        _, axes = plt.subplots(num_nodes, 1, figsize=(15, 1.5 * num_nodes), sharex=False)

        if num_nodes == 1:
            axes = [axes]  # Ensure axes is iterable

        all_end_dates = [df['timestamp'].max() for df in node_dfs.values()]
        global_end = max(all_end_dates)
        global_start = global_end - pd.Timedelta(days=30)

        for ax, (_, df) in zip(axes, node_dfs.items()):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')

            df_30 = df[(df['timestamp'] >= global_start) & (df['timestamp'] <= global_end)]

            # Compute ON/OFF intervals
            intervals = []
            last_state = None
            last_time = None

            for _, row in df_30.iterrows():
                if last_state is None:
                    last_state = row['power']
                    last_time = row['timestamp']
                elif row['power'] != last_state:
                    intervals.append((last_time, row['timestamp'], last_state))
                    last_state = row['power']
                    last_time = row['timestamp']

            intervals.append((last_time, df_30['timestamp'].iloc[-1], last_state))

            # Plot intervals
            for start, end, state in intervals:
                color = 'green' if state == 1 else 'red'
                ax.barh(0, end - start, left=start, height=0.4, color=color)

            node_name_from_df = df['nodename'].iloc[0]  # first row's nodename

            # Format X-axis
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
            ax.set_yticks([])
            ax.set_title(f"{node_name_from_df} (Green=ON, Red=OFF)")
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            ax.grid(axis='x', which='minor', color='lightgray', linestyle='--', linewidth=0.5)

            # Set the same start/end date for all
            ax.set_xlim(global_start, global_end)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')  # Rotate dates for readability

        plt.tight_layout()
        plt.savefig('report.png')
        plt.show()
        plt.close()