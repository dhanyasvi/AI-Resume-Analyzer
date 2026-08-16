"use client";

import { ChangeEvent, FormEvent, useState } from "react";

type Result = { filename: string; extracted_characters: number; overall_score: number; ats_score: number; job_match_score: number; detected_skills: string[]; missing_skills: string[]; keyword_results: { keyword: string; found: boolean }[]; strengths: string[]; improvements: string[]; executive_assessment: string; priority_actions: string[]; rewritten_bullet: string; score_breakdown: Record<string, number>; coverage_items: { label: string; score: number; detail: string; status: string }[]; resume_metrics: Record<string, number>; ai_enabled: boolean };

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

function ScoreCard({ label, score, accent }: { label: string; score: number; accent: string }) {
  return <article className="score-card"><span>{label}</span><strong>{score}{label === "Job-resume match" ? "%" : " / 100"}</strong><div className="track"><i style={{ width: `${score}%`, backgroundColor: accent }} /></div></article>;
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function selectFile(event: ChangeEvent<HTMLInputElement>) {
    const selected = event.target.files?.[0] ?? null;
    setFile(selected); setResult(null); setError("");
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!file) { setError("Choose a PDF resume first."); return; }
    setLoading(true); setError("");
    const body = new FormData(); body.append("resume", file); body.append("job_description", jobDescription);
    try {
      const response = await fetch(`${API_URL}/api/analyze`, { method: "POST", body });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Analysis failed. Please try again.");
      setResult(data);
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : "Something went wrong."); }
    finally { setLoading(false); }
  }

  return <main>
    <header><a className="brand" href="#top"><span>✦</span> ResumeAI</a><p>Practical resume feedback, explained clearly.</p></header>
    <section id="top" className="hero"><div><p className="eyebrow">AI RESUME ANALYZER</p><h1>Turn your resume into a stronger application.</h1><p className="lead">Upload a PDF and compare it with a job description. You’ll get ATS signals, skill gaps, keyword coverage, and specific next steps.</p></div>
      <form onSubmit={submit} className="upload-card"><label className="file-zone"><input type="file" accept="application/pdf" onChange={selectFile} /><b>{file ? file.name : "Choose your resume PDF"}</b><small>{file ? `${Math.ceil(file.size / 1024)} KB selected` : "PDF only · maximum 10 MB"}</small></label><label>Job description <em>(optional)</em><textarea value={jobDescription} onChange={(event) => setJobDescription(event.target.value)} placeholder="Paste the job description to calculate your job match…" rows={5} /></label>{error && <p className="error">{error}</p>}<button disabled={loading}>{loading ? "Analyzing resume…" : "Analyze my resume →"}</button></form>
    </section>
    {result ? <section className="results" aria-live="polite"><div className="result-heading"><div><p className="eyebrow">ANALYSIS COMPLETE</p><h2>{result.filename}</h2><p>{result.extracted_characters.toLocaleString()} characters extracted from your resume.</p></div><div className="report-actions"><span className="ready">{result.ai_enabled ? "AI insights enabled" : "Smart local analysis"}</span><button className="print" type="button" onClick={() => window.print()}>Print / save PDF</button></div></div>
      <div className="scores"><ScoreCard label="Overall resume score" score={result.overall_score} accent="#635bff" /><ScoreCard label="ATS compatibility" score={result.ats_score} accent="#e58b23" /><ScoreCard label="Job-resume match" score={result.job_match_score} accent="#008a64" /></div>
      <section className="insight"><div className="score-orb" style={{ background: `conic-gradient(#635bff ${result.overall_score}%, #e9ebf4 0)` }}><span>{result.overall_score}</span></div><div><p className="eyebrow">EXECUTIVE ASSESSMENT</p><h3>{result.executive_assessment}</h3><p>{result.ai_enabled ? "Guidance was generated from your resume and measured signals." : "Add an OpenAI API key later to unlock tailored AI coaching."}</p></div></section>
      <section className="breakdown"><h3>Score breakdown</h3>{Object.entries(result.score_breakdown).map(([name, value]) => <div key={name}><span>{name}</span><div className="track"><i style={{ width: `${value}%` }} /></div><b>{value}</b></div>)}</section>
      <section className="metric-strip" aria-label="Resume metrics">{Object.entries(result.resume_metrics).map(([name, value]) => <div key={name}><b>{value}</b><span>{name.replace("_", " ")}</span></div>)}</section>
      <section className="coverage"><div className="section-title"><div><p className="eyebrow">RESUME HEALTH CHECK</p><h3>Coverage that recruiters and ATS systems look for</h3></div><p>Each area is calculated from your uploaded resume.</p></div><div className="coverage-grid">{result.coverage_items.map((item) => <article key={item.label}><div className="coverage-top"><span className={`status ${item.status.toLowerCase().replace(" ", "-")}`}>{item.status}</span><b>{item.score}</b></div><h4>{item.label}</h4><p>{item.detail}</p><div className="track"><i style={{ width: `${item.score}%` }} /></div></article>)}</div></section>
      <div className="analysis-grid"><article><h3>Detected skills</h3><div className="tags">{result.detected_skills.length ? result.detected_skills.map((skill) => <span key={skill}>{skill}</span>) : <p>No matching skills detected yet.</p>}</div></article><article><h3>Missing / recommended skills</h3><div className="tags warm">{result.missing_skills.length ? result.missing_skills.map((skill) => <span key={skill}>{skill}</span>) : <p>Great coverage for the skills named in this job description.</p>}</div></article><article><h3>Resume strengths</h3><ul>{result.strengths.map((item) => <li key={item}>{item}</li>)}</ul></article><article><h3>Top improvements</h3><ul className="improvements">{result.improvements.map((item) => <li key={item}>{item}</li>)}</ul></article></div>
      <section className="coaching"><article><p className="eyebrow">PRIORITY ACTION PLAN</p><h3>Make these edits first</h3><ol>{result.priority_actions.map((item) => <li key={item}>{item}</li>)}</ol></article><article><p className="eyebrow">STRONGER BULLET EXAMPLE</p><h3>Use a result-first format</h3><blockquote>{result.rewritten_bullet}</blockquote><small>Replace the bracketed details with facts from your own experience.</small></article></section>
      {result.keyword_results.length > 0 && <article className="keywords"><h3>Job-description keyword analysis</h3>{result.keyword_results.map((item) => <div key={item.keyword}><span>{item.keyword}</span><b className={item.found ? "found" : "missing"}>{item.found ? "Found" : "Missing"}</b></div>)}</article>}
    </section> : <section className="how"><h2>What you’ll receive</h2><div><article><b>01</b><h3>ATS readiness</h3><p>Clear checks for sections, contact details, skills, and measurable achievements.</p></article><article><b>02</b><h3>Skill gap analysis</h3><p>See the relevant skills you already show and those you may need to add.</p></article><article><b>03</b><h3>Better next steps</h3><p>Get focused suggestions you can use to improve your next application.</p></article></div></section>}
  </main>;
}
