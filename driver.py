import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------------
# COLOR MAP (SAFE)
# ----------------------------------
def assign_color(val_type, values):
    cl = []
    for val in values:
        parts = val.split()
        abbr = parts[1][:3].upper() if len(parts) > 1 else parts[0][:3].upper()

        if abbr in ['NOR','PIA']: cl.append('#FF8700')
        elif abbr in ['VER','TSU']: cl.append('#1E41FF')
        elif abbr in ['HAM','LEC']: cl.append('#DC0000')
        elif abbr in ['RUS','ANT']: cl.append('#00D2BE')
        elif abbr in ['ALO','STR']: cl.append('#006F62')
        elif abbr in ['ALB','SAI']: cl.append('#005AFF')
        elif abbr in ['GAS','COL','DOO']: cl.append('#0090FF')
        elif abbr in ['HUL','BOR']: cl.append('#00FF00')
        elif abbr in ['OCO','BEA']: cl.append('#858E95')
        elif abbr in ['LAW','HAD']: cl.append('#2B4562')
        else: cl.append('#888888')

    return cl


# ----------------------------------
# DRIVER ANALYSIS RENDERER
# ----------------------------------
def render_driver_analysis(raceResults, sprintResults, calendar, analysis_type, highlight_driver, opacity):

    # ----------------------------------
    # Driver Standings
    # ----------------------------------
    if analysis_type == "Driver Standings":

        race = raceResults.rename(columns={'Points':'Race Points'})
        sprint = sprintResults.rename(columns={'Points':'Sprint Points'})

        racePts = race.groupby('Driver')['Race Points'].sum()
        sprintPts = sprint.groupby('Driver')['Sprint Points'].sum()

        standings = pd.concat([racePts, sprintPts], axis=1).fillna(0).astype(int)
        standings['Total Points'] = standings.sum(axis=1)
        standings = standings.sort_values('Total Points', ascending=False)
        standings.insert(0, 'Rank', range(1, len(standings) + 1))
        standings.reset_index(inplace=True)

        st.dataframe(standings, use_container_width=True)

    # ----------------------------------
    # Race Winner Counts
    # ----------------------------------
    elif analysis_type == "Race Winner Counts":

        winners = raceResults[raceResults['Position'] == '1']
        counts = winners['Driver'].value_counts().sort_values(ascending=True)

        colors = assign_color('drivers', counts.index)

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor("#15151e")
        ax.set_facecolor("#15151e")

        ax.barh(
            [d.split()[1] for d in counts.index],
            counts.values,
            color=colors
        )

        for i, v in enumerate(counts.values):
            ax.text(v - 0.15, i, v, va='center', color='white', fontsize=13)

        ax.set_title(
            "Formula 1 – 2025 Season – Race Winner Counts",
            fontsize=16,
            color='white',
            pad=12
        )

        ax.set_xlabel("Number of Race Wins", fontsize=13, color='white')
        ax.set_ylabel("Drivers", fontsize=13, color='white')
        ax.tick_params(colors='white', labelsize=12)
        ax.set_xlim(0, counts.values.max() + 0.5)
        ax.grid(axis='y', alpha=0.25, linestyle='--')
        st.pyplot(fig)


    # ----------------------------------
    # Driver Podium Counts
    # ----------------------------------
    elif analysis_type == "Driver Podium Counts":

        podiums = raceResults[raceResults['Position'].isin(['1','2','3'])]
        counts = podiums['Driver'].value_counts().sort_values(ascending=True)
        colors = assign_color('drivers', counts.index)

        fig, ax = plt.subplots(figsize=(12, 6))

        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh(
            [d.split()[1] for d in counts.index],
            counts.values,
            color=colors
        )

        for i, v in enumerate(counts.values):
            ax.text(v - 0.2, i, v, va='center', color='white', fontsize=13)

        ax.set_title(
            "Formula 1 – 2025 Season – Podium Finish Counts",
            fontsize=16,
            color='white',
            pad=12
        )

        ax.set_xlabel("Number of Podium Finishes", fontsize=13, color='white')
        ax.set_ylabel("Drivers", fontsize=13, color='white')

        max_val = counts.values.max()
        ax.set_xticks(range(0, max_val + 2, 2))
        ax.tick_params(colors='white', labelsize=12)
        ax.grid(axis='y', alpha=0.25, linestyle='--')
        st.pyplot(fig)

    # ----------------------------------
    # Points Progression (DRIVER)
    # ----------------------------------
    elif analysis_type == "Points Progression":
            race = raceResults.rename(columns={'Points': 'Race Points'})
            sprint = sprintResults.rename(columns={'Points': 'Sprint Points'})

            pts = pd.merge(
                race[['Track', 'Driver', 'Race Points']],
                sprint[['Track', 'Driver', 'Sprint Points']],
                on=['Track', 'Driver'],
                how='left'
            ).fillna(0)

            pts['Total'] = pts['Race Points'] + pts['Sprint Points']
            tracks = race['Track'].unique()

            top10 = (pts.groupby('Driver')['Total'].sum().sort_values(ascending=False).head(10).index)

            fig, ax = plt.subplots(figsize=(14, 6))
            fig.patch.set_facecolor("#1E1E2B")  ##1E1E2B
            ax.set_facecolor("#15151e")   ##15151d
            colors = assign_color('drivers', top10)


            for i, d in enumerate(top10):
                y = (pts[pts['Driver'] == d].groupby('Track')['Total'].sum().reindex(tracks, fill_value=0).cumsum())

                is_highlight = (d == highlight_driver)

                ax.plot(tracks, y, color=colors[i], linewidth=3
                     if is_highlight else 1.5,
                    alpha=1.0 if is_highlight else opacity,
                    label=d.split()[1]
                )

            ax.set_title(
                "Formula 1 – 2025 Season – Points Progression (Top 10 Drivers)",
                color='white',
                fontsize=16,
                pad=12
            )

            ax.set_xlabel("Grand Prix", color='white', fontsize=12)
            ax.set_ylabel("Championship Points", color='white', fontsize=12)
            ax.set_xticks(range(len(tracks)))
            ax.set_xticklabels(tracks, rotation=55, ha='right', fontsize=10, color='white')

            max_pts = int(pts.groupby('Driver')['Total'].sum().max())
            ax.set_yticks(range(0, max_pts + 50, 50))
            ax.tick_params(colors='white')
            ax.grid(alpha=0.25)

            legend = ax.legend(ncol=5, fontsize=10, frameon=False, loc='upper left')

            for text in legend.get_texts():
                text.set_color('white')

            st.pyplot(fig)

    # ----------------------------------
    # Top 10 Finish Counts
    # ----------------------------------
    elif analysis_type == "Top 10 Finish Counts":

        top10 = list(map(str, range(1, 11)))

        topTenFinishes = (raceResults[raceResults['Position'].isin(top10)]['Driver'].value_counts()
            .sort_values(ascending=True))

        colors = assign_color('drivers', topTenFinishes.index)
        fig, ax = plt.subplots(figsize=(11, 6.5))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh(
            [driver.split()[1] for driver in topTenFinishes.index],
            topTenFinishes.values,
            color=colors
        )

        for i, val in enumerate(topTenFinishes.values):
            shift = 0.5 if val >= 10 else 0.35
            ax.text(val - shift, i, val, color='white', fontsize=14, va='center')

        ax.set_xlim(0, topTenFinishes.values.max() + 0.5)

        ax.set_title(
            "Formula 1 – 2025 Season – Top 10 Finish Counts",
            color='white',
            fontsize=16,
            pad=12)

        ax.set_xlabel("Top 10 Finishes", color='white')
        ax.set_ylabel("Drivers", color='white')

        ax.grid(False)
        ax.tick_params(colors='white')
        st.pyplot(fig)


    # ----------------------------------
    # Fastest Lap Counts
    # ----------------------------------
    
    elif analysis_type == "Fastest Lap Counts":

        fastestLaps = raceResults[raceResults['Set Fastest Lap'] == 'Yes']
        fastestLapCnt = (fastestLaps['Driver'].value_counts().sort_values(ascending=True))

        colors = assign_color('drivers', fastestLapCnt.index)
        fig, ax = plt.subplots(figsize=(11, 5))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh([driver.split()[1] for driver in fastestLapCnt.index],
            fastestLapCnt.values,
            color=colors
        )

        for i, val in enumerate(fastestLapCnt.values):
            ax.text(val - 0.15, i, val, color='white', fontsize=14, va='center')

        ax.set_xlim(0, fastestLapCnt.values.max() + 0.3)

        ax.set_title(
            "Formula 1 – 2025 Season – Fastest Lap Counts",
            color='white',
            fontsize=16,
            pad=12
        )

        ax.set_xlabel("Fastest Laps", color='white')
        ax.set_ylabel("Drivers", color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

    # ----------------------------------
    # DNFs by Drivers
    # ----------------------------------

    elif analysis_type == "DNFs by Drivers":

        DNF = raceResults[raceResults['Time/Retired'] == 'DNF']
        DNFdriver = DNF['Driver'].value_counts()

        colors = assign_color('drivers', DNFdriver.index)

        fig, ax = plt.subplots(figsize=(11, 7))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh([driver.split()[1] for driver in DNFdriver.index],
            DNFdriver.values,
            color=colors
        )

        for i, v in enumerate(DNFdriver.values):
            ax.text(v - 0.18, i + 0.21, v, color='white',fontsize=14)

        ax.set_xlim(0, DNFdriver.values.max() + 0.3)
        ax.set_title(
            "Formula 1 – 2025 Season – DNFs by Drivers",
            color='white',
            fontsize=16
        )
        ax.set_xlabel("DNFs", color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

    # ----------------------------------
    # Finish Positions (Top 10)
    # ----------------------------------

    elif analysis_type == "Finish Positions (Top 10)":

        finishPos = raceResults[['Track', 'Driver', 'Position']].copy()

        finishPos['Position'] = finishPos['Position'].replace({
            'NC': 20,
            'DQ': 20,
            'DSQ': 20,
            'DNF': 20
        })

        finishPos['Position'] = pd.to_numeric(
            finishPos['Position'],
            errors='coerce'
        )

        trackOrder = raceResults['Track'].unique()

        racePts = raceResults.rename(columns={'Points': 'Race Points'}) \
                            .groupby('Driver')['Race Points'].sum()

        sprintPts = sprintResults.rename(columns={'Points': 'Sprint Points'}) \
                                .groupby('Driver')['Sprint Points'].sum()

        finalStandings = (pd.concat([racePts, sprintPts], axis=1).fillna(0))
        finalStandings['Total Points'] = finalStandings.sum(axis=1)

        driverOrder = finalStandings.sort_values(
            'Total Points', ascending=False
        ).head(10).index

        colors = assign_color('drivers', driverOrder)

        fig, ax = plt.subplots(figsize=(16, 7))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.set_xlim(-0.2, len(trackOrder) - 0.3)
        ax.set_ylim(20.2, 0.75)

        for i, driver in enumerate(driverOrder):

            driverPos = (finishPos[finishPos['Driver'] == driver].groupby('Track')['Position'].mean()
                .reindex(trackOrder, fill_value=20).values
            )

            abbr = driver.split()[1].upper()[:3]

            linestyle = '--' if abbr in ['PIA', 'VER', 'NOR'] else '-'
            is_highlight = (driver == highlight_driver)

            ax.plot(trackOrder, driverPos, color=colors[i], marker='o',
                markersize=9 if is_highlight else 6,
                linewidth=3 if is_highlight else 1.5,
                alpha=1.0 if is_highlight else opacity,
                linestyle=linestyle,
                label=driver.split()[1]
            )

        ax.set_title(
            "Formula 1 – 2025 Season – Race Finish Positions (Top 10 Drivers)",
            fontsize=18,
            color='white'
        )
        ax.set_xlabel("Tracks", fontsize=13, color='white')
        ax.set_ylabel("Finish Position", fontsize=13, color='white')

        ax.set_xticks(range(len(trackOrder)))
        ax.set_xticklabels(trackOrder, rotation=55, fontsize=10, color='white')
        ax.set_yticks(range(1, 21))
        ax.tick_params(colors='white')

        legend = ax.legend(loc='upper center',
            bbox_to_anchor=(0.5, -0.31),
            ncol=5,
            fontsize=11,
            frameon=False
        )

        for text in legend.get_texts():text.set_color('white')

        ax.grid(alpha=0.2)
        plt.subplots_adjust(bottom=0.30)
        st.pyplot(fig)

