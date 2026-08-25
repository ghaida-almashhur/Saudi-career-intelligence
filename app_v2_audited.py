import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"

jobs = pd.read_csv(DATA / "jadarat_detailed_enriched.csv")
families = pd.read_csv(DATA / "career_match_family_features_v0_1.csv")
occ = pd.read_csv(DATA / "official_occupation_market_summary.csv", dtype={"official_occupation_code": str})
official_skills = pd.read_csv(DATA / "data_ai_official_family_skills.csv")
sequence = pd.read_csv(DATA / "skill_learning_sequence_heuristic_v0_1.csv")
stats_path = pd.read_csv(DATA / "statistics_career_pathway_v0_1.csv")
stat_skills = pd.read_csv(DATA / "statistics_official_family_skills.csv")
major_seed = pd.read_csv(DATA / "official_major_role_seed.csv")

st.set_page_config(page_title="Saudi Career Intelligence | ذكاء المسار المهني السعودي",
                   page_icon="📊", layout="wide")

st.markdown("""
<style>
.block-container{max-width:1250px;padding-top:1.5rem;padding-bottom:4rem}
.hero{padding:2.2rem 2.4rem;border:1px solid rgba(128,128,128,.25);border-radius:22px;margin-bottom:1.2rem}
.hero h1{font-size:2.6rem;margin-bottom:.4rem}.hero p{font-size:1.08rem;opacity:.82;max-width:900px}
.badge{display:inline-block;padding:.25rem .7rem;border:1px solid rgba(128,128,128,.35);border-radius:999px;margin:.35rem .35rem 0 0;font-size:.86rem}
.small-note{font-size:.86rem;opacity:.72}
div[data-testid="stMetric"]{border:1px solid rgba(128,128,128,.22);padding:1rem;border-radius:16px}
</style>
""", unsafe_allow_html=True)

lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True, label_visibility="collapsed")
AR = lang == "العربية"
def t(ar,en): return ar if AR else en
def money(x):
    if pd.isna(x): return t("غير متاح","N/A")
    return f"{x:,.0f} ر.س" if AR else f"SAR {x:,.0f}"

family_ar = {
"Administration & Support":"الإدارة والدعم","Data & Analytics":"البيانات والتحليلات",
"Education":"التعليم","Engineering":"الهندسة","Finance & Accounting":"المالية والمحاسبة",
"Healthcare":"الرعاية الصحية","Human Resources":"الموارد البشرية",
"Legal & Compliance":"القانون والامتثال","Operations & Supply Chain":"العمليات وسلاسل الإمداد",
"Other":"أخرى","Sales & Marketing":"المبيعات والتسويق","Technology":"التقنية"}

major_ar = {
"Statistics":"الإحصاء","Economics":"الاقتصاد","Data Science":"علوم البيانات",
"Quantitative Methods":"الأساليب الكمية",
"Operations and Information Management":"إدارة العمليات والمعلومات",
"Other / Not loaded":"أخرى / غير محمّل في الأدلة الحالية"
}

skill_ar = {
"Artificial intelligence, machine learning & deep learning application":"تطبيقات الذكاء الاصطناعي وتعلم الآلة والتعلم العميق",
"Data analytics":"تحليلات البيانات","Data cleaning":"تنظيف البيانات",
"Data collection and analysis":"جمع البيانات وتحليلها","Data design":"تصميم البيانات",
"Data engineering":"هندسة البيانات","Data management":"إدارة البيانات",
"Data preparation":"إعداد البيانات","Data processing":"معالجة البيانات",
"Data visualization and storyboarding":"تصور البيانات والسرد القصصي",
"Data warehousing":"مستودعات البيانات","Database management & configuration":"إدارة قواعد البيانات وتهيئتها",
"Database modelling":"نمذجة قواعد البيانات","Knowledge of big data tools and platforms":"معرفة أدوات ومنصات البيانات الضخمة",
"Machine learning":"تعلم الآلة","Natural language processing":"معالجة اللغة الطبيعية"
}

stat_skill_ar = {
"Big data analysis":"تحليل البيانات الضخمة","Budget management":"إدارة الميزانية",
"Business continuity strategy and planning":"استراتيجية وتخطيط استمرارية الأعمال",
"Business data analysis":"تحليل بيانات الأعمال","Business environment analysis":"تحليل بيئة الأعمال",
"Business innovation and improvement":"ابتكار وتحسين الأعمال","Business needs analysis":"تحليل احتياجات الأعمال",
"Business negotiation":"التفاوض التجاري","Business risk assessment and management":"تقييم وإدارة مخاطر الأعمال",
"Data analytics and system optimization":"تحليلات البيانات وتحسين الأنظمة","Research data analysis":"تحليل بيانات البحوث",
"Research findings communication":"التواصل بنتائج البحوث","Strategic research":"البحث الاستراتيجي"
}

role_ar = {
"Data Analyst":"محلل بيانات","Data Scientist":"عالم بيانات","Business Analyst":"محلل أعمال",
"Business Analytics Specialist":"أخصائي تحليلات أعمال","Data Engineer":"مهندس بيانات"
}
fit_ar = {"Strong":"قوي","Adjacent":"مجاور"}
evidence_ar = {
"Explicit official program eligibility + official statistical-analysis family role":"أهلية رسمية صريحة + دور رسمي ضمن عائلة التحليل الإحصائي",
"Official Statistical Analysis and Interpretation family role":"دور رسمي ضمن عائلة التحليل الإحصائي والتفسير",
"Official Business Analysis family is on the same career pathway map":"عائلة تحليل الأعمال موجودة على خريطة المسار المهني نفسها",
"Official Data Collection and Management family is on the same career pathway map":"عائلة جمع البيانات وإدارتها موجودة على خريطة المسار المهني نفسها"
}
direction_ar = {
"Start with data analysis, cleaning, visualization, SQL/database concepts":"ابدأ بتحليل البيانات وتنظيفها وتصورها ومفاهيم SQL وقواعد البيانات",
"Add machine learning, advanced modelling and programming":"أضف تعلم الآلة والنمذجة المتقدمة والبرمجة",
"Add requirements analysis, business context and stakeholder communication":"أضف تحليل المتطلبات وفهم الأعمال والتواصل مع أصحاب المصلحة",
"Add business analytics, forecasting and decision support":"أضف تحليلات الأعمال والتنبؤ ودعم القرار",
"Add databases, data engineering and warehousing":"أضف قواعد البيانات وهندسة البيانات ومستودعات البيانات"
}

# The source has a mixture of Arabic labels and noisy/truncated English transliterations.
# Use clean Arabic source labels as the canonical city list, with a curated English display map.
raw_cities = jobs["city_standard"].dropna().astype(str).unique()
city_options = sorted([x for x in raw_cities if any("\u0600" <= c <= "\u06ff" for c in x)])
city_en = {
"الرياض":"Riyadh","جدة":"Jeddah","مكة المكرمة":"Makkah","المدينة المنورة":"Madinah",
"الدمام":"Dammam","الخبر":"Khobar","الظهران":"Dhahran","الجبيل":"Jubail","الطائف":"Taif",
"تبوك":"Tabuk","أبها":"Abha","ابها":"Abha","الباحة":"Al Baha","بريدة":"Buraidah",
"حائل":"Hail","حفر الباطن":"Hafar Al Batin","خميس مشيط":"Khamis Mushait",
"سكاكا":"Sakaka","نجران":"Najran","ينبع":"Yanbu","الخرج":"Al Kharj","القطيف":"Qatif",
"الهفوف":"Al Hofuf","القنفذة":"Al Qunfudhah"}
def city_label(x): return x if AR else city_en.get(x, x)

st.markdown(f"""
<div class="hero" {'dir="rtl"' if AR else ''}>
<div class="small-note">{t('منتج بحثي للملف المهني · المملكة العربية السعودية','PORTFOLIO RESEARCH PRODUCT · SAUDI ARABIA')}</div>
<h1>{t('ذكاء المسار المهني السعودي','Saudi Career Intelligence')}</h1>
<p>{t('من بيانات الوظائف الخام إلى قرارات مهنية مبنية على الأدلة لحديثي التخرج. استكشف سهولة الوصول للوظائف المبتدئة، وسياق الرواتب، والمسارات المهنية السعودية الرسمية، وفجوات المهارات بوضوح.','From raw job postings to evidence-aware career decisions for fresh graduates. Explore entry-level accessibility, salary context, official Saudi career pathways, and transparent skill-gap guidance.')}</p>
<span class="badge">Python</span><span class="badge">SQL</span><span class="badge">Statistics</span>
<span class="badge">{t('الأطر السعودية الرسمية','Official Saudi frameworks')}</span><span class="badge">Streamlit</span>
</div>""", unsafe_allow_html=True)

m1,m2,m3,m4=st.columns(4)
m1.metric(t("إعلانات وظيفية مفصلة","Detailed postings"), f"{len(jobs):,}")
m2.metric(t("نسبة الوظائف المبتدئة","Entry-level share"), f"{jobs['entry_level_flag'].mean()*100:.1f}%")
m3.metric(t("وظائف لا تتطلب خبرة","Zero-experience roles"), f"{int(jobs['zero_experience_flag'].sum()):,}")
m4.metric(t("وسيط الراتب المعلن","Median listed salary"), money(jobs["salary_sar"].median()))
st.caption(t("هذه الأرقام تمثل عينة جدارات المستخدمة في المشروع، وليست كامل سوق العمل السعودي.",
             "Snapshot reflects the detailed Jadarat sample used in this prototype; it is not the entire Saudi labor market."))

tab1,tab2,tab3,tab4,tab5=st.tabs([
t("🎯 ملاءمة المسار","🎯 Career Match"), t("📈 سوق حديثي التخرج","📈 Fresh Graduate Market"),
t("🧭 المسارات الرسمية","🧭 Official Pathways"), t("📊 خريج الإحصاء","📊 Statistics Graduate"),
t("🔎 المنهجية والمصادر","🔎 Methodology & Sources")])

with tab1:
    st.subheader(t("ابنِ ملفك لقياس ملاءمتك مع السوق","Build your market-fit profile"))
    st.caption(t("النتيجة مؤشر سياقي مبني على بيانات المشروع وليست احتمالًا لقبولك في وظيفة.",
                 "The result is a project-based market-context score, not a probability that an employer will hire you."))
    left,right=st.columns([.9,1.6],gap="large")
    with left:
        major_opts = major_seed["major"].dropna().drop_duplicates().tolist() + ["Other / Not loaded"]
        major = st.selectbox(t("التخصص","Major"), major_opts,
                             format_func=lambda x: major_ar.get(x,x) if AR else x,
                             index=major_opts.index("Statistics") if "Statistics" in major_opts else 0)
        default_city=city_options.index("جدة") if "جدة" in city_options else 0
        city=st.selectbox(t("المدينة المفضلة","Preferred city"), city_options,
                          format_func=city_label, index=default_city)
        experience=st.number_input(t("سنوات الخبرة","Years of experience"),0.0,30.0,0.0,1.0)
        fams=sorted(jobs["career_family"].dropna().unique())
        default_fam=fams.index("Data & Analytics") if "Data & Analytics" in fams else 0
        target=st.selectbox(t("المجال المهني المستهدف","Target career family"), fams,
                            format_func=lambda x: family_ar.get(x,x) if AR else x, index=default_fam)
        salary_expectation=st.number_input(t("الراتب الشهري المتوقع (ر.س)","Expected monthly salary (SAR)"),
                                           min_value=0,value=0,step=500)

    fr=families[families["career_family"]==target].iloc[0]
    market=float(fr["market_opportunity_score"]) if pd.notna(fr["market_opportunity_score"]) else 50.0
    subset=jobs[jobs["career_family"]==target].copy()

    # Correct direction: a candidate meets a requirement when candidate experience >= required experience.
    req=subset["experience_years"].dropna()
    exp_score=float((req <= experience).mean()*100) if len(req) else 50.0

    city_subset=jobs[jobs["city_standard"]==city]
    city_entry=float(city_subset["entry_level_flag"].mean()*100) if len(city_subset) else 50.0
    city_volume=min(100.0,np.log1p(len(city_subset))/np.log1p(max(1,len(jobs)))*100)
    city_score=.65*city_entry+.35*city_volume

    sal_score=50.0
    if salary_expectation>0:
        pool=subset[subset["city_standard"]==city]["salary_sar"].dropna()
        if len(pool)<5: pool=subset["salary_sar"].dropna()
        if len(pool) and pool.median()>0:
            med=float(pool.median())
            sal_score=max(0.0,100-abs((salary_expectation/med)-1)*100)

    score=round(.45*market+.30*exp_score+.15*city_score+.10*sal_score,1)

    with right:
        st.markdown("### "+t("نتيجتك","Your result"))
        a,b=st.columns(2)
        a.metric(t("مؤشر الملاءمة","Market-fit score"),f"{score}%")
        b.metric(t("فرص السوق","Market Opportunity"),f"{market:.0f}/100")
        st.progress(min(max(score/100,0),1))
        c,d=st.columns(2)
        c.metric(t("نسبة الوظائف المبتدئة","Entry-level share"),f"{fr['family_entry_share']*100:.1f}%")
        d.metric(t("وسيط الراتب المرصود","Observed median salary"),money(fr["family_median_salary"]))
        st.info(t(f"تحتوي العينة على {len(subset):,} إعلانًا ضمن {family_ar.get(target,target)}. استخدم النتيجة لفهم سياق السوق، لا كتوقع للتوظيف.",
                  f"The sample contains {len(subset):,} postings under {target}. Use the score as market context, not as a hiring prediction."))

        if major != "Other / Not loaded" and target == "Data & Analytics":
            st.success(t(
                f"يوجد في الأدلة الرسمية المحمّلة ارتباط صريح بين تخصص {major_ar.get(major,major)} ومهنة محلل البيانات. هذا دليل أهلية/ارتباط، وليس ضمان توظيف.",
                f"The loaded official evidence explicitly links {major} with the Data Analyst occupation. This is eligibility/alignment evidence, not a hiring guarantee."
            ))
        elif major == "Other / Not loaded":
            st.caption(t(
                "عدم وجود تخصصك في القائمة لا يعني أنه غير مناسب؛ يعني فقط أن المشروع لم يحمّل له دليلًا رسميًا كافيًا بعد.",
                "Not seeing your major here does not mean it is unsuitable; it only means the project has not loaded enough official major-level evidence for it yet."
            ))

with tab2:
    st.subheader(t("واقع سوق حديثي التخرج","Fresh Graduate Reality"))
    c1,c2=st.columns(2,gap="large")
    clean=jobs[jobs["city_standard"].isin(city_options)].copy()
    with c1:
        ct=(clean[clean["entry_level_flag"]].groupby("city_standard")
            .agg(Postings=("job_title","size"),Median_Salary=("salary_sar","median"))
            .sort_values("Postings",ascending=False).head(10).reset_index())
        ct["city_standard"]=ct["city_standard"].map(city_label)
        ct=ct.rename(columns={"city_standard":t("المدينة","City"),"Postings":t("الإعلانات","Postings"),
                              "Median_Salary":t("وسيط الراتب","Median salary")})
        st.markdown("#### "+t("أكبر أسواق الوظائف المبتدئة حسب المدينة","Largest entry-level city markets"))
        st.dataframe(ct,use_container_width=True,hide_index=True)
    with c2:
        ft=families[["career_family","family_postings","family_entry_share","family_median_salary"]].copy()
        ft=ft.sort_values("family_entry_share",ascending=False)
        ft["share"]=(ft["family_entry_share"]*100).round(1)
        ft["career_family"]=ft["career_family"].map(lambda x:family_ar.get(x,x) if AR else x)
        ft=ft.rename(columns={"career_family":t("المجال المهني","Career family"),
                              "family_postings":t("الإعلانات","Postings"),
                              "share":t("نسبة الوظائف المبتدئة","Entry-level share"),
                              "family_median_salary":t("وسيط الراتب","Median salary")})
        st.markdown("#### "+t("سهولة الوصول حسب المجال المهني","Accessibility by career family"))
        st.dataframe(ft[[t("المجال المهني","Career family"),t("الإعلانات","Postings"),
                         t("نسبة الوظائف المبتدئة","Entry-level share"),t("وسيط الراتب","Median salary")]],
                     use_container_width=True,hide_index=True)
    st.caption(t("تصنيف المجالات المهنية طبقة تحليلية في المشروع وليس التصنيف المهني السعودي الرسمي.",
                 "Career-family classification is a project analysis layer, not the official Saudi occupation taxonomy."))

with tab3:
    st.subheader(t("المسارات السعودية الرسمية للبيانات والذكاء الاصطناعي","Official Saudi Data & AI pathways"))
    if AR:
        labels=occ["official_occupation_ar"]+" — "+occ["official_occupation_en"]+" ("+occ["official_occupation_code"].astype(str)+")"
    else:
        labels=occ["official_occupation_en"]+" — "+occ["official_occupation_ar"]+" ("+occ["official_occupation_code"].astype(str)+")"
    selected=st.selectbox(t("استكشف مهنة رسمية","Explore an official occupation"),labels.tolist())
    idx=labels[labels==selected].index[0]
    row=occ.loc[idx]
    a,b,c,d=st.columns(4)
    a.metric(t("العينة الحديثة","Recent sample"),int(row["recent_postings"]) if pd.notna(row["recent_postings"]) else 0)
    b.metric(t("العينة المفصلة","Detailed sample"),int(row["detailed_postings"]) if pd.notna(row["detailed_postings"]) else 0)
    c.metric(t("نسبة الوظائف المبتدئة","Entry-level share"),
             f"{row['entry_level_share_pct']:.1f}%" if pd.notna(row["entry_level_share_pct"]) else t("غير متاح","N/A"))
    reliable=pd.notna(row["median_salary_sar"]) and pd.notna(row["detailed_postings"]) and row["detailed_postings"]>=5
    d.metric(t("وسيط الراتب","Median salary"),
             money(row["median_salary_sar"]) if reliable else t("عينة غير كافية","Insufficient sample"))
    if pd.notna(row["median_salary_sar"]) and not reliable:
        st.caption(t("أُخفي رقم الراتب لأن عدد الإعلانات المفصلة أقل من 5؛ عرض رقم من إعلان واحد مثلًا قد يكون مضللًا.",
                     "Salary is suppressed because fewer than 5 detailed postings are available; a value based on one posting can be misleading."))

    st.markdown("### "+t("تغطية مهارات عائلة البيانات والذكاء الاصطناعي الرسمية","Official Data & AI family skill coverage"))
    opts=official_skills["skill_name_en"].dropna().tolist()
    selected_skills=st.multiselect(
        t("المهارات التي لديك","Skills you already have"), opts,
        format_func=lambda x: skill_ar.get(x,x) if AR else x
    )
    coverage=round(len(selected_skills)/len(opts)*100,1) if opts else 0
    st.metric(t("تغطية مهارات العائلة","Family-level skill coverage"),f"{coverage}%")
    st.progress(coverage/100 if opts else 0)
    missing=[x for x in opts if x not in selected_skills]
    if missing:
        ranked=sequence[sequence["skill_name_en"].isin(missing)].sort_values("priority_order")
        if len(ranked):
            nxt = ranked.iloc[0]["skill_name_en"]
            st.success(t("المهارة التالية المقترحة: ","Prototype next skill: ")+f"**{skill_ar.get(nxt,nxt) if AR else nxt}**")
        with st.expander(t("عرض المهارات غير المحددة","See missing family-level skills")):
            st.write("، ".join(skill_ar.get(x,x) for x in missing) if AR else ", ".join(missing))
    st.warning(t("تغطية المهارات مبنية على أدلة رسمية على مستوى العائلة الوظيفية، أما ترتيب المهارة التالية فهو قاعدة توصية خاصة بالنموذج.",
                 "Skill coverage uses official job-family-level evidence; the next-skill order is a product heuristic, not an official ranking."))

with tab4:
    st.subheader(t("مسار خريج الإحصاء","Statistics Graduate Pathway"))
    st.write(t("يبرز المشروع لخريجي الإحصاء المسارات الأساسية والمجاورة المدعومة بالأدلة، بدل افتراض وجود مسار مهني واحد فقط.",
               "For Statistics graduates, the product highlights evidence-backed core and adjacent directions instead of assuming one career outcome."))

    display_path = stats_path[["target_role","fit_level","official_evidence","development_direction"]].copy()
    if AR:
        display_path["target_role"] = display_path["target_role"].map(lambda x: role_ar.get(x,x))
        display_path["fit_level"] = display_path["fit_level"].map(lambda x: fit_ar.get(x,x))
        display_path["official_evidence"] = display_path["official_evidence"].map(lambda x: evidence_ar.get(x,x))
        display_path["development_direction"] = display_path["development_direction"].map(lambda x: direction_ar.get(x,x))
        display_path = display_path.rename(columns={
            "target_role":"المسار المستهدف","fit_level":"مستوى الملاءمة",
            "official_evidence":"الدليل الرسمي","development_direction":"اتجاه التطوير"
        })
    st.dataframe(display_path,use_container_width=True,hide_index=True)

    st.markdown("### "+t("مهارات عائلة التحليل الإحصائي الرسمية","Official Statistical Analysis family skills"))
    skills_list = stat_skills["skill_name_en"].dropna().tolist()
    st.write("، ".join(stat_skill_ar.get(x,x) for x in skills_list) if AR else ", ".join(skills_list))
    st.info(t("قد تختلف متطلبات الوظائف الفردية عن أدلة إطار العائلة المهنية.",
              "Individual vacancy requirements can differ from career-family framework evidence."))

with tab5:
    st.subheader(t("كيف تقرأ هذا المنتج","How to read this product"))
    st.markdown(t(
"""**أدلة السوق المرصودة** تأتي من عينات جدارات المستخدمة في المشروع.

**الأدلة الرسمية** تأتي من أطر المهن والمهارات التابعة لوزارة الموارد البشرية والتنمية الاجتماعية.

**قواعد توصية المنتج** أنشئت لهذا النموذج الأولي ويتم توضيحها بصراحة.

يستخدم مؤشر فرص حديثي التخرج سهولة الدخول، والطلب، والراتب، والانتشار الجغرافي، وتنوع أصحاب العمل. وتم اختبار استقرار الترتيب عبر **3,000 محاكاة للأوزان**. نمذجة الرواتب تعرض ارتباطات لا علاقات سببية.""",
"""**Observed market evidence** comes from the Jadarat samples used in the project.

**Official evidence** comes from Saudi HRSD occupation and skills frameworks.

**Product heuristics** are recommendation rules created for this prototype and are labeled as such.

The Fresh Graduate Opportunity Index uses entry accessibility, demand, salary, geographic breadth and employer diversity. Its rankings were stress-tested across **3,000 weight simulations**. Salary modelling is presented as association, not causation."""))
    st.markdown("### "+t("عائلات المصادر الرسمية","Official source families"))
    st.write(t("تصنيف المهارات السعودي لوزارة الموارد البشرية · إطار مهارات الخدمات المهنية والاستشارية · مكتبة البيانات المفتوحة للوزارة",
               "HRSD Saudi Skills Taxonomy · Professional & Consulting Services Skills Framework · HRSD Open Data Library"))
    st.warning(t("هذا نموذج بحثي للملف المهني، وليس ضمانًا للتوظيف أو خدمة حكومية رسمية أو تمثيلًا كاملًا لجميع الوظائف السعودية.",
                 "This is a portfolio research prototype, not a hiring guarantee, official government service, or complete representation of all Saudi vacancies."))

st.divider()
st.caption(t("ذكاء المسار المهني السعودي · نموذج بحثي للملف المهني · مصمم بمنهج قائم على الأدلة",
             "Saudi Career Intelligence · Portfolio research prototype · Evidence-aware by design"))
