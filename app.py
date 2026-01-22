import streamlit as st
import pandas as pd
from driver import render_driver_analysis
from team import render_team_analysis

st.set_page_config(
    page_title="Formula 1 – 2025 Dashboard",
    layout="wide"
)

# ----------------------------------
# THEME
# ----------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; }
html, body { background-color: #0E1117; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align:center;'>🏎️ Formula 1 – 2025 Season Dashboard</h2>",
    unsafe_allow_html=True
)
st.markdown("---")

# ----------------------------------
# LOAD DATA (ONCE)
# ----------------------------------
@st.cache_data
def load_data():
    calendar = pd.read_csv("Formula1_Calendar.csv")
    drivers = pd.read_csv("Formula1_Drivers.csv")
    race = pd.read_csv("Formula1_RaceResults.csv")
    sprint = pd.read_csv("Formula1_SprintResults.csv")
    return calendar, drivers, race, sprint

calendar, drivers, raceResults, sprintResults = load_data()

# ----------------------------------
# SIDEBAR – ANALYSIS CONTROL
# ----------------------------------
with st.sidebar:

    st.markdown("## 📊 Analysis Control")

    category = st.radio(
        "Select Category",
        ["Overview", "Drivers", "Teams","Engine"],
        index=0
    )

    st.markdown("---")

    # -------------------------------
    # DRIVER CONTROLS (INSIDE SIDEBAR)
    # -------------------------------
    if category == "Drivers":

            driver_analysis = st.selectbox(
                "Driver Analysis",
                [
                    "Driver Standings",
                    "Race Winner Counts",
                    "Driver Podium Counts",
                    "Top 10 Finish Counts",
                    "Fastest Lap Counts",
                    "DNFs by Drivers",
                    "DNFs per Track",
                    "Points Progression",
                    "Finish Positions (Top 10)"
                ]
            )

            if driver_analysis in [
                "Points Progression",
                "Finish Positions (Top 10)"
            ]:
                highlight_driver = st.selectbox(
                    "Highlight Driver",
                    sorted(raceResults["Driver"].unique())
                )

                opacity = st.slider(
                    "Fade Other Drivers",
                    0.1, 1.0, 0.3, 0.1
                )
            else:
                highlight_driver = None
                opacity = 1.0

    # -------------------------------
    # TEAM CONTROLS (INSIDE SIDEBAR)
    # -------------------------------
    elif category == "Teams":

            team_analysis = st.selectbox(
                "Team Analysis",
                [
                    "Team Standings",
                    "Team Podium Counts",
                    "DNFs by Team",
                    "DNFs per Track",
                    "Points Progression"
                ]
            )

            if team_analysis == "Points Progression":

                highlight_team = st.selectbox(
                    "Highlight Team",
                    sorted(raceResults["Team"].unique())
                )

                opacity = st.slider(
                    "Fade Other Teams",
                    0.1, 1.0, 0.3, 0.1
                )

            else:
                highlight_team = None
                opacity = 1.0



# ----------------------------------
# ROUTING (THIS WAS THE MISSING PART)
# ----------------------------------
if category == "Overview":

    st.subheader("🏆 2025 Season Overview")

    st.markdown("---")

    col1, col2 = st.columns(2)

    # -------------------------------
    # DRIVER CHAMPION
    # -------------------------------
    with col1:
        st.markdown("### 🥇 World Driver Champion")
        st.image(
            "https://mb.com.ph/manilabulletin/uploads/images/2025/12/08/64073.webp",
            use_container_width=True
        )
        st.markdown("**Lando Norris**")
        st.caption("McLaren • 2025 World Champion")

    # -------------------------------
    # CONSTRUCTOR CHAMPION
    # -------------------------------
    with col2:
        st.markdown("### 🏗️ Constructor Champion")
        st.image(
            "https://images.gmanews.tv/webpics/2025/10/2025-10-05T144110Z_760779854_UP1ELA514SLYL_RTRMADP_3_MOTOR-F1-SINGAPORE_2025_10_05_22_53_41.jpeg",
            use_container_width=True
        )
        st.markdown("**McLaren F1 Team**")
        st.caption("2025 Constructors' Champion")

    st.markdown("---")

    st.info(
        "This dashboard provides an in-depth analysis of the 2025 Formula 1 season, "
        "covering driver performance, team dominance, race trends, and championship progression."
    )

elif category == "Drivers":
    render_driver_analysis(
        raceResults=raceResults,
        sprintResults=sprintResults,
        calendar=calendar,
        analysis_type=driver_analysis,
        highlight_driver=highlight_driver,
        opacity=opacity
    )

elif category == "Teams":
    render_team_analysis(
    raceResults=raceResults,
    sprintResults=sprintResults,
    calendar=calendar,
    analysis_type=team_analysis,
    highlight_team=highlight_team,
    opacity=opacity
    )


elif category == "Engine":

    st.subheader("⚙️ Formula 1 – 2025 Engine Suppliers")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    # -------------------------------
    # FERRARI
    # -------------------------------
    with col1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/de/c/c0/Scuderia_Ferrari_Logo.svg",
            width=230 
        )
        st.markdown("### Ferrari")
        st.caption("Ferrari • Haas • Kick Sauber")

    # -------------------------------
    # MERCEDES
    # -------------------------------
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Mercedes-Logo.svg/512px-Mercedes-Logo.svg.png",
            use_container_width=True
        )
        st.markdown("### Mercedes")
        st.caption("Mercedes • McLaren • Aston Martin • Williams")

    # -------------------------------
    # HONDA RBPT
    # -------------------------------
    with col3:
        st.image(
            "https://pngimg.com/uploads/car_logo/car_logo_PNG1643.png",
            use_container_width=True
        )
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### Honda RBPT")
        st.caption("Red Bull Racing • RB")

    # -------------------------------
    # RENAULT
    # -------------------------------
    with col4:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Renault_2009_logo.svg/500px-Renault_2009_logo.svg.png",
            use_container_width=True
        )
        st.markdown("### Renault")
        st.caption("Alpine")

    st.markdown("---")

    st.info(
        "Engine suppliers play a crucial role in Formula 1 performance. "
        "The 2025 season features four manufacturers powering the entire grid."
    )


# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:12px;'>Formula 1 – 2025 Data Analysis Dashboard</p>",
    unsafe_allow_html=True
)
