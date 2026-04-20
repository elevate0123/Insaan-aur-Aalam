#import "@preview/fontawesome:0.2.0": *

#let primary_color = rgb("#222222")
#let secondary_color = rgb("#666666")

#let heading_font = "Lato"
#let body_font = "Lato"

#set document(
  title: "Almaas Shaikh - Resume",
  author: "Almaas Shaikh",
)

#set page(
  margin: (x: 0.8in, y: 0.8in),
  background: none
)

#set text(
  font: body_font,
  size: 10.5pt,
  fill: primary_color
)

// Helper function for contact info
#let contact_info(icon, text) = {
  box(
    text(
      size: 9pt,
      fill: secondary_color,
      [#icon #h(4pt) #text]
    )
  )
}

// Re-usable function for section headings
#let section_heading(title) = {
  text(font: heading_font, size: 11pt, weight: "bold", fill: primary_color, title)
  line(length: 100%, stroke: 0.5pt + primary_color)
  v(12pt)
}

// Re-usable function for experience entries
#let experience_entry(title, company, date, location, items) = {
  v(8pt)
  text(font: heading_font, size: 10pt, weight: "bold")[#title]
  text(font: heading_font, size: 10pt, weight: "bold", fill: secondary_color)[ | #company]
  grid(
    columns: (1fr, auto),
    text(size: 9pt, fill: secondary_color)[#date],
    text(size: 9pt, fill: secondary_color)[#location],
  )
  v(4pt)
  for item in items {
    [• #h(6pt) #item]
    v(4pt)
  }
}

// Header
align(center, {
  text(font: heading_font, size: 28pt, weight: "bold", fill: primary_color, "Almaas Shaikh")
  v(12pt)
  text(size: 10pt, fill: secondary_color, "almaas0123@gmail.com | 88491 40665")
  v(16pt)
})

// Main Content in a two-column layout
grid(
  columns: (65%, 35%),
  column-gutter: 24pt,
  // Left Column
  [
    #section_heading("EXPERIENCE")
    #experience_entry(
      "CIVIC TECH (NDA)", "BUSINESS ANALYST CONSULTANT",
      "Nov 2024 - Present", "Ahmedabad",
      (
        "Consolidated inputs from government agencies, nonprofits, devs into a unified backlog, reducing development rework by 50%.",
        "Set up a structured feedback process using Airtable & automation, accelerating triage & resolution of usability issues by 40%.",
        "Improved mobile onboarding for underserved users by refining requirements & acceptance criteria, cutting user drop-off by 33%.",
        "Led field-based UAT across kiosk and mobile platforms, identifying and resolving 10+ critical usability blockers pre-launch.",
      )
    )

    #experience_entry(
      "TECSTUB", "BUSINESS ANALYST",
      "Nov 2023 - Oct 2024", "Ahmedabad",
      (
        "Spearheaded the strategic migration of a legacy monolithic platform to a microservices architecture, reducing feature deployment cycles from monthly to weekly and cutting production incidents by 40%.",
        "Automated warehouse operations with a new RPA system, cutting handling costs by 20% while scaling capacity to 5K+ daily orders.",
        "Built and prioritized the product backlog with 200+ user stories and clear BPMN flows, reducing costly development rework by 30%.",
        "Led the API integration of 10+ new partners (insurance, logistics, payments), boosting transaction processing speed by 20%.",
      )
    )

    #experience_entry(
      "STEAMROLL TECHNOLOGIES", "BUSINESS ANALYST",
      "Jul 2018 - Oct 2023", "Ahmedabad",
      (
        "Launched a G2C-G2B GRAS unified payment portal, onboarding 30+ departments & 3K+ users within the first 6 months, reducing payment related queries by 40%.",
        "Led the company's transition to Agile, moving teams to Jira & Confluence and coaching Scrum practices to speed up feature delivery by 25%.",
        "Managed G2B RFP process from creation to vendor selection, securing a partner to deliver the final project 15% under budget.",
        "Improved client satisfaction by 30% through clear presentations to senior officials and proactive post-launch support.",
      )
    )

    #section_heading("PREVIOUS EXPERIENCE")
    #experience_entry(
        "Empowering CPO", "Business Analyst",
        "Jan-Jun 2018", "",
        (
            "Delivered $18,000 cost savings (12%) on a $150K budget by creating smarter procurement strategies for CPG and aviation sectors. Developed go-to-market strategy through competitive pricing and positioning analysis.",
        )
    )
    #experience_entry(
        "Gujarat Agro Industries Corporation", "Management Trainee",
        "Jul-Sep 2017", "",
        (
            "Created a new credit policy that reduced late payments by 20% in the first quarter. Supported ERP system rollout with testing and operational feedback.",
        )
    )
     #experience_entry(
        "Peerbits Solutions", "Content Writer",
        "May-Aug 2016", "",
        (
            "Boosted web traffic by 25% and CTR by 30% through SEO-optimized blog posts (20+). Conducted keyword research to enhance content strategy.",
        )
    )
     #experience_entry(
        "RapidOps Inc.", "Software Engineer Intern",
        "Jan-Apr 2016", "",
        (
            "Developed custom BigCommerce APIs using the MEAN stack. Improved site performance by reducing load times by 40%.",
        )
    )

  ],

  // Right Column
  [
    #section_heading("SUMMARY")
    text(size: 9pt, "A strategic Business Analyst who excels at translating complex business needs into high-impact technical solutions. Thrives on bridging the gap between stakeholders and development teams to optimize workflows, clarify requirements, and deliver user-centric products that create tangible business value.")
    v(16pt)

    #section_heading("EDUCATION")
    #v(4pt)
    text(font: heading_font, size: 10pt, weight: "bold", "POST GRADUATION")
    text(size: 9pt, "MBA - FINANCE & MARKETING")
    text(size: 9pt, "2018 | BKSBM, Gujarat University")
    v(8pt)
    text(font: heading_font, size: 10pt, weight: "bold", "GRADUATION")
    text(size: 9pt, "BE - COMPUTER SCIENCE")
    text(size: 9pt, "2016 | AIT, Gujarat Technological University")
    v(16pt)

    #section_heading("KEY SKILLS")
    #v(4pt)
    text(weight: "bold", size: 10pt, "PRODUCT & AGILE")
    text(size: 9pt, "Product Roadmapping\nStakeholder Management\nUser Persona & Journey Mapping\nMarket Research & Competitive Analysis\nAgile & Scrum Methodologies\nUser Stories, Epics & Acceptance Criteria\nBacklog Grooming & Prioritisation")
    v(8pt)
    text(weight: "bold", size: 10pt, "BUSINESS ANALYSIS")
    text(size: 9pt, "Requirements Elicitation & Documentation\nProcess Modelling\nGap Analysis & Solution Design\nUAT Planning & Execution\nCross-Functional Team Leadership")
    v(16pt)

    #section_heading("TOOLS & TECH")
    #v(4pt)
    [#text(weight: "bold", size: 9pt, "Product Management - ") Jira • Confluence • Trello • Productboard]
    v(4pt)
    [#text(weight: "bold", size: 9pt, "Collaboration & Design - ") Miro • Figma • Lucidchart • GitHub • Notion • Asana]
    v(4pt)
    [#text(weight: "bold", size: 9pt, "Data & Analytics - ") SQL • Power BI • GA • Mixpanel • Looker Studio • Hotjar]
    v(16pt)

    #section_heading("COMPETITIVE AWARDS")
    #v(4pt)
    text(size: 9pt, "Open Gov Data Hackathon\nSmart India Hackathon\nNational Case Studies (under publication)")
  ]
)