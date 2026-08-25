import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"

jobs = pd.read_csv(DATA / "jadarat_detailed_enriched.csv")
families = pd.read_csv(DATA / "career_match_family_features_v0_1.csv")
cities = pd.read_csv(DATA / "career_match_city_features_v0_1.csv")
occ = pd.read_csv(DATA / "official_occupation_market_summary.csv", dtype={"official_occupation_code": str})
official_skills = pd.read_csv(DATA / "data_ai_official_family_skills.csv")
sequence = pd.read_csv(DATA / "skill_learning_sequence_heuristic_v0_1.csv")
stats_path = pd.read_csv(DATA / "statistics_career_pathway_v0_1.csv")
stat_skills = pd.read_csv(DATA / "statistics_official_family_skills.csv")

st.set_page_config(
    page_title="Saudi Career Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 2rem; padding-bottom: 4rem;}
.hero {
    padding: 2.2rem 2.4rem;
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 22px;
    margin-bottom: 1.2rem;
}
.hero h1 {font-size: 2.6rem; margin-bottom: .4rem;}
.hero p {font-size: 1.08rem; opacity: .82; max-width: 850px;}
.badge {
    display:inline-block; padding:.25rem .7rem; border:1px solid rgba(128,128,128,.35);
    border-radius:999px; margin-right:.35rem; margin-top:.35rem; font-size:.86rem;
}
.small-note {font-size:.86rem; opacity:.72;}
div[data-testid="stMetric"] {
    border:1px solid rgba(128,128,128,.22);
    padding:1rem; border-radius:16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="small-note">PORTFOLIO RESEARCH PRODUCT · SAUDI ARABIA</div>
  <h1>Saudi Career Intelligence</h1>
  <p>From raw job postings to evidence-aware career decisions for fresh graduates.
  Explore entry-level accessibility, salary context, official Saudi career pathways,
  and transparent skill-gap guidance.</p>
  <span class="badge">Python</span>
  <span class="badge">SQL</span>
  <span class="badge">Statistics</span>
  <span class="badge">Official Saudi frameworks</span>
  <span class="badge">Streamlit</span>
</div>
""", unsafe_allow_html=True)

# Top market snapshot
m1,m2,m3,m4 = st.columns(4)
m1.metric("Detailed postings", f"{len(jobs):,}")
m2.metric("Entry-level share", f"{jobs['entry_level_flag'].mean()*100:.1f}%")
m3.metric("Zero-experience roles", f"{int(jobs['zero_experience_flag'].sum()):,}")
m4.metric("Median listed salary", f"SAR {jobs['salary_sar'].median():,.0f}")

st.caption("Snapshot reflects the detailed Jadarat sample used in this prototype; it is not the entire Saudi labor market.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Career Match", "📈 Fresh Graduate Market", "🧭 Official Pathways",
    "📊 Statistics Graduate", "🔎 Methodology & Sources"
])

with tab1:
    st.subheader("Build your market-fit profile")
    left, right = st.columns([0.9, 1.6], gap="large")
    with left:
        major = st.text_input("Major", placeholder="Statistics")
        city = st.selectbox("Preferred city", sorted(jobs["city_standard"].dropna().astype(str).unique()))
        experience = st.number_input("Years of experience", min_value=0.0, max_value=30.0, value=0.0, step=1.0)
        target = st.selectbox("Target career family", sorted(jobs["career_family"].dropna().unique()))
        salary_expectation = st.number_input("Expected monthly salary (SAR)", min_value=0, value=0, step=500)

    family_row = families[families["career_family"] == target].iloc[0]
    city_row = cities[cities["city_standard"] == city]
    market_score = float(family_row["market_opportunity_score"])
    subset = jobs[jobs["career_family"] == target].copy()
    req = subset["experience_years"].dropna()

    if len(req):
        experience_score = float((req >= experience).mean()*100) if experience <= req.median() else float((req <= experience).mean()*100)
    else:
        experience_score = 50.0
    city_score = float(city_row.iloc[0]["city_access_score"]) if len(city_row) else 50.0

    salary_score = 50.0
    if salary_expectation > 0:
        pool = subset[subset["city_standard"] == city]["salary_sar"].dropna()
        if len(pool) < 5:
            pool = subset["salary_sar"].dropna()
        if len(pool):
            med = float(pool.median())
            salary_score = max(0, 100 - abs((salary_expectation/med)-1)*100)

    score = round(0.45*market_score + 0.30*experience_score + 0.15*city_score + 0.10*salary_score, 1)

    with right:
        st.markdown("### Your result")
        a,b = st.columns(2)
        a.metric("Career Match", f"{score}%")
        b.metric("Market Opportunity", f"{market_score:.0f}/100")
        st.progress(min(max(score/100,0),1))
        c,d = st.columns(2)
        c.metric("Entry-level share", f"{family_row['family_entry_share']*100:.1f}%")
        d.metric("Observed median salary", f"SAR {family_row['family_median_salary']:,.0f}")
        st.info(
            f"The detailed sample contains {len(subset):,} postings classified under **{target}**. "
            "Use this score as market context, not as a probability that an employer will hire you."
        )

with tab2:
    st.subheader("Fresh Graduate Reality")
    col1,col2 = st.columns(2, gap="large")
    with col1:
        city_table = (
            jobs[jobs["entry_level_flag"]]
            .groupby("city_standard")
            .agg(Postings=("job_title","size"), Median_Salary=("salary_sar","median"))
            .sort_values("Postings", ascending=False)
            .head(10)
            .reset_index()
        )
        st.markdown("#### Largest entry-level city markets")
        st.dataframe(city_table, use_container_width=True, hide_index=True)
    with col2:
        fam_table = (
            families[["career_family","family_postings","family_entry_share","family_median_salary"]]
            .copy()
            .sort_values("family_entry_share", ascending=False)
        )
        fam_table["Entry-level share"] = (fam_table["family_entry_share"]*100).round(1)
        fam_table = fam_table.rename(columns={
            "career_family":"Career family",
            "family_postings":"Postings",
            "family_median_salary":"Median salary"
        })
        st.markdown("#### Accessibility by career family")
        st.dataframe(
            fam_table[["Career family","Postings","Entry-level share","Median salary"]],
            use_container_width=True, hide_index=True
        )
    st.caption("Career-family classification is a documented project layer and is not the official Saudi occupation taxonomy.")

with tab3:
    st.subheader("Official Saudi Data & AI pathways")
    labels = occ["official_occupation_en"] + " — " + occ["official_occupation_ar"] + " (" + occ["official_occupation_code"].astype(str) + ")"
    selected = st.selectbox("Explore an official occupation", labels.tolist())
    idx = labels[labels == selected].index[0]
    row = occ.loc[idx]

    a,b,c,d = st.columns(4)
    a.metric("Recent sample", int(row["recent_postings"]) if pd.notna(row["recent_postings"]) else 0)
    b.metric("Detailed sample", int(row["detailed_postings"]) if pd.notna(row["detailed_postings"]) else 0)
    c.metric("Entry-level share", f"{row['entry_level_share_pct']:.1f}%" if pd.notna(row["entry_level_share_pct"]) else "N/A")
    d.metric("Median salary", f"SAR {row['median_salary_sar']:,.0f}" if pd.notna(row["median_salary_sar"]) else "N/A")

    st.markdown("### Official Data & AI family skill coverage")
    opts = official_skills["skill_name_en"].tolist()
    selected_skills = st.multiselect("Skills you already have", opts)
    coverage = round(len(selected_skills)/len(opts)*100,1) if opts else 0
    missing = [x for x in opts if x not in selected_skills]
    st.metric("Family-level skill coverage", f"{coverage}%")
    st.progress(coverage/100 if opts else 0)

    if missing:
        ranked = sequence[sequence["skill_name_en"].isin(missing)].sort_values("priority_order")
        if len(ranked):
            st.success(f"Prototype next skill: **{ranked.iloc[0]['skill_name_en']}**")
        with st.expander("See missing family-level skills"):
            st.write(", ".join(missing))
    else:
        st.success("All currently loaded family-level skills selected.")

    st.warning(
        "Skill coverage is based on official **job-family-level** evidence. "
        "The 'next skill' order is a transparent product heuristic, not an official priority ranking."
    )

with tab4:
    st.subheader("Statistics Graduate Pathway")
    st.write(
        "For Statistics graduates, the product highlights evidence-backed core and adjacent directions "
        "instead of assuming there is only one career outcome."
    )
    st.dataframe(
        stats_path[["target_role","fit_level","official_evidence","development_direction"]],
        use_container_width=True, hide_index=True
    )
    st.markdown("### Official Statistical Analysis family skills")
    st.write(", ".join(stat_skills["skill_name_en"].tolist()))
    st.info("Individual vacancy requirements can differ from career-family framework evidence.")

with tab5:
    st.subheader("How to read this product")
    st.markdown("""
**Observed market evidence** comes from the Jadarat samples used in the project.

**Official evidence** comes from Saudi HRSD occupation and skills frameworks.

**Product heuristics** are recommendation rules created for this prototype and are labeled as such.

The Fresh Graduate Opportunity Index uses entry accessibility, demand, salary, geographic breadth and employer diversity.
Its rankings were stress-tested across **3,000 weight simulations**. Salary modelling is presented as association, not causation.
""")
    st.markdown("### Official source families")
    st.write("HRSD Saudi Skills Taxonomy · Professional & Consulting Services Skills Framework · HRSD Open Data Library")
    st.warning(
        "This is a portfolio research prototype, not a hiring guarantee, official government service, "
        "or complete representation of all Saudi vacancies."
    )

st.divider()
st.caption("Saudi Career Intelligence · Portfolio release candidate · Evidence-aware by design")
