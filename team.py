import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------
# TEAM COLOR MAP (FIXED & CONSISTENT)
# ----------------------------------
def assign_team_color(teams):
    color_map = {
        "Red Bull Racing": "#1E41FF",    
        "Racing Bulls F1 Team": "#2B4562",
        "Ferrari": "#DC0000", 
        "Mercedes": "#00D2BE", 
        "McLaren": "#FF8700",      
        "Aston Martin": "#006F62",     
        "Alpine": "#0090FF",          
        "Williams Racing": "#005AFF",    
        "Haas F1 Team": "#B6BABD",    
        "Kick Sauber": "#00FF00"  
    }

    return [color_map.get(team, "#000000") for team in teams]


# ----------------------------------
# TEAM ANALYSIS RENDERER
# ----------------------------------
def render_team_analysis(raceResults, sprintResults, analysis_type, highlight_team, opacity):

    raceResults = raceResults.rename(columns={'Points':'Race Points'})
    sprintResults = sprintResults.rename(columns={'Points':'Sprint Points'})


    # -----------------------------
    # TEAM STANDINGS
    # -----------------------------
    if analysis_type == "Team Standings":

        racePts = raceResults.groupby('Team')['Race Points'].sum()
        sprintPts = sprintResults.groupby('Team')['Sprint Points'].sum()

        standings = pd.concat([racePts, sprintPts], axis=1).fillna(0).astype(int)
        standings['Total Points'] = standings.sum(axis=1)
        standings = standings.sort_values('Total Points', ascending=False)
        standings.reset_index(inplace=True)

        st.dataframe(standings, use_container_width=True)

    # -----------------------------
    # TEAM PODIUM COUNTS
    # -----------------------------
    elif analysis_type == "Team Podium Counts":

        podiums = raceResults[raceResults['Position'].isin(['1','2','3'])]
        counts = podiums['Team'].value_counts()

        colors = assign_team_color(counts.index)

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh(counts.index, counts.values, color=colors)

        ax.set_title(
            "Podium Finish Counts (Teams)",
            color='white',
            fontsize=16
        )
        ax.set_xlabel("Podium Finishes", color='white')
        ax.set_ylabel("Teams", color='white')

        ax.tick_params(colors='white')
        ax.grid(axis='x', alpha=0.25)

        st.pyplot(fig)


    # -----------------------------
    # DNFs BY TEAM
    # -----------------------------
    elif analysis_type == "DNFs by Team":

        dnf = raceResults[raceResults['Time/Retired'] == 'DNF']
        counts = dnf['Team'].value_counts()

        colors = assign_team_color(counts.index)

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh(
            counts.index,
            counts.values,
            color=colors
        )

        ax.set_title(
            "DNFs by Team",
            fontsize=16,
            color='white'
        )
        ax.set_xlabel("Number of DNFs", color='white')
        ax.set_ylabel("Teams", color='white')

        ax.tick_params(colors='white')
        ax.grid(axis='x', alpha=0.25)

        st.pyplot(fig)


    # ----------------------------------
    # DNFs per Track
    # ----------------------------------

    elif analysis_type == "DNFs per Track":

        DNF = raceResults[raceResults['Time/Retired'] == 'DNF']
        DNFtrack = DNF['Track'].value_counts()

        norm = plt.Normalize(
            vmin=DNFtrack.values.min(),
            vmax=DNFtrack.values.max()
        )
        cmap = plt.get_cmap('Reds')
        colors = cmap(norm(DNFtrack.values))

        fig, ax = plt.subplots(figsize=(11, 6))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        ax.barh(DNFtrack.index, DNFtrack.values, color=colors, edgecolor='white')

        for i, v in enumerate(DNFtrack.values):
            ax.text(v - 0.2, i + 0.23, v, color='white', fontsize=14)

        ax.set_xlim(0, DNFtrack.values.max() + 0.3)
        ax.set_title(
            "Formula 1 – 2025 Season – DNFs by Track",
            color='white',
            fontsize=16
        )
        ax.set_xlabel("DNFs", color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)


    # -----------------------------
    # Points Progression
    # -----------------------------
    elif analysis_type == "Points Progression":

        race_team_track = (
            raceResults
            .groupby(['Track', 'Team'], as_index=False)['Race Points']
            .sum()
        )

        sprint_team_track = (
            sprintResults
            .groupby(['Track', 'Team'], as_index=False)['Sprint Points']
            .sum()
        )

        teamTrackPts = pd.merge(
            race_team_track,
            sprint_team_track,
            on=['Track', 'Team'],
            how='left'
        ).fillna(0)

        teamTrackPts['Total'] = (
            teamTrackPts['Race Points'] + teamTrackPts['Sprint Points']
        )

        trackOrder = raceResults['Track'].drop_duplicates().values

        teamTotals = (
            teamTrackPts
            .groupby('Team')['Total']
            .sum()
            .sort_values(ascending=False)
        )

        topTeams = teamTotals.head(10).index
        colors = assign_team_color(topTeams)

        fig, ax = plt.subplots(figsize=(14, 6))
        fig.patch.set_facecolor('#15151e')
        ax.set_facecolor('#15151e')

        for i, team in enumerate(topTeams):

            y = (
                teamTrackPts[teamTrackPts['Team'] == team]
                .set_index('Track')
                .reindex(trackOrder, fill_value=0)['Total']
                .cumsum()
            )

            is_highlight = (team == highlight_team)

            ax.plot(
                trackOrder,
                y,
                color=colors[i],
                linewidth=3 if is_highlight else 1.5,
                alpha=1.0 if is_highlight else opacity,
                label=team
            )

        ax.set_title(
            "Team Points Progression (Race + Sprint)",
            fontsize=16,
            color='white'
        )
        ax.set_xlabel("Tracks", color='white')
        ax.set_ylabel("Points", color='white')

        ax.set_xticks(range(len(trackOrder)))
        ax.set_xticklabels(trackOrder, rotation=45, ha='right', color='white')

        ax.tick_params(colors='white')

        ax.grid(
            axis='y',
            linestyle='--',
            linewidth=0.6,
            color='#2a2a35',
            alpha=0.6
        )

        legend = ax.legend(ncol=2, frameon=False)
        for text in legend.get_texts():
            text.set_color('white')

        plt.subplots_adjust(bottom=0.25)
        st.pyplot(fig)
