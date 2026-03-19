use chrono::{Duration, NaiveDate};
use std::collections::HashSet;
use std::env;
use std::fs;
use std::path::{Path, PathBuf};

struct Config {
    date: NaiveDate,
    lookback_days: i64,
}

#[derive(Default)]
struct DayData {
    completed: Vec<String>,
    decisions: Vec<String>,
    blockers: Vec<String>,
    questions: Vec<String>,
    candidate_tasks: Vec<String>,
}

fn usage(bin: &str) -> String {
    format!("Usage: {bin} --date YYYY-MM-DD [--lookback-days N]")
}

fn parse_args() -> Result<Config, String> {
    let mut date: Option<NaiveDate> = None;
    let mut lookback_days: i64 = 1;

    let args: Vec<String> = env::args().collect();
    let mut i = 1;

    while i < args.len() {
        match args[i].as_str() {
            "--date" => {
                if i + 1 >= args.len() {
                    return Err("Missing value for --date".to_string());
                }
                date = Some(
                    NaiveDate::parse_from_str(&args[i + 1], "%Y-%m-%d")
                        .map_err(|_| format!("Invalid date: {}", args[i + 1]))?,
                );
                i += 2;
            }
            "--lookback-days" => {
                if i + 1 >= args.len() {
                    return Err("Missing value for --lookback-days".to_string());
                }
                lookback_days = args[i + 1]
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid --lookback-days: {}", args[i + 1]))?;
                if lookback_days < 1 {
                    return Err("--lookback-days must be >= 1".to_string());
                }
                i += 2;
            }
            "-h" | "--help" => {
                return Err(usage(args.first().map(String::as_str).unwrap_or("next-day-summary")));
            }
            other => {
                return Err(format!(
                    "Unknown argument: {other}\n{}",
                    usage(args.first().map(String::as_str).unwrap_or("next-day-summary"))
                ));
            }
        }
    }

    let date = date.ok_or_else(|| {
        format!(
            "--date is required\n{}",
            usage(args.first().map(String::as_str).unwrap_or("next-day-summary"))
        )
    })?;

    Ok(Config {
        date,
        lookback_days,
    })
}

fn repo_root() -> Result<PathBuf, String> {
    let mut dir = env::current_dir().map_err(|e| format!("Failed to read current directory: {e}"))?;

    loop {
        if dir.join(".git").exists() && dir.join("AGENTS.md").exists() {
            return Ok(dir);
        }
        if !dir.pop() {
            break;
        }
    }

    Err("Could not locate repository root (expected .git and AGENTS.md).".to_string())
}

fn push_unique(target: &mut Vec<String>, item: &str, seen: &mut HashSet<String>) {
    let trimmed = item.trim();
    if trimmed.is_empty() {
        return;
    }

    let key = trimmed.to_lowercase();
    if seen.insert(key) {
        target.push(trimmed.to_string());
    }
}

fn parse_daily_note(content: &str) -> DayData {
    let mut data = DayData::default();

    let mut section = String::new();
    let mut seen_completed = HashSet::new();
    let mut seen_decisions = HashSet::new();
    let mut seen_blockers = HashSet::new();
    let mut seen_questions = HashSet::new();
    let mut seen_candidates = HashSet::new();

    for raw_line in content.lines() {
        let line = raw_line.trim();

        if let Some(heading) = line.strip_prefix("## ") {
            section = heading.trim().to_lowercase();
            continue;
        }

        let bullet = line
            .strip_prefix("- ")
            .or_else(|| line.strip_prefix("* "))
            .map(str::trim);

        let Some(item) = bullet else {
            continue;
        };

        if section.contains("work completed")
            || section == "completed"
            || section.contains("done")
            || section.contains("highlights")
        {
            push_unique(&mut data.completed, item, &mut seen_completed);
        }

        if section.contains("decision") {
            push_unique(&mut data.decisions, item, &mut seen_decisions);
        }

        if section.contains("risk") || section.contains("blocker") {
            push_unique(&mut data.blockers, item, &mut seen_blockers);
        }

        if section.contains("open question") || section == "questions" || section.contains("question") {
            push_unique(&mut data.questions, item, &mut seen_questions);
        }

        if section.contains("candidate next task")
            || section.contains("candidate next tasks")
            || section == "next task"
            || section == "next tasks"
            || section.contains("todo")
            || section.contains("to do")
        {
            push_unique(&mut data.candidate_tasks, item, &mut seen_candidates);
        }
    }

    data
}

fn dedupe_preserve(items: Vec<String>) -> Vec<String> {
    let mut seen = HashSet::new();
    let mut out = Vec::new();

    for item in items {
        let key = item.to_lowercase();
        if seen.insert(key) {
            out.push(item);
        }
    }

    out
}

fn markdown_bullets(items: &[String], empty_line: &str) -> String {
    if items.is_empty() {
        return format!("- {empty_line}\n");
    }

    let mut out = String::new();
    for item in items {
        out.push_str("- ");
        out.push_str(item);
        out.push('\n');
    }
    out
}

fn markdown_task_bullets(items: &[String], empty_line: &str) -> String {
    if items.is_empty() {
        return format!("- [ ] {empty_line}\n");
    }

    let mut out = String::new();
    for item in items {
        out.push_str("- [ ] ");
        out.push_str(item);
        out.push('\n');
    }
    out
}

fn write_file(path: &Path, content: &str) -> Result<(), String> {
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent).map_err(|e| format!("Failed to create directory {}: {e}", parent.display()))?;
    }
    fs::write(path, content).map_err(|e| format!("Failed to write {}: {e}", path.display()))
}

fn run(config: Config) -> Result<(), String> {
    let root = repo_root()?;
    let daily_dir = root.join("40_work_tracking").join("daily");
    let summaries_dir = root.join("40_work_tracking").join("summaries");
    let tasks_dir = root.join("40_work_tracking").join("tasks");

    let mut source_days: Vec<NaiveDate> = Vec::new();
    let mut completed: Vec<String> = Vec::new();
    let mut decisions: Vec<String> = Vec::new();
    let mut blockers: Vec<String> = Vec::new();
    let mut questions: Vec<String> = Vec::new();
    let mut candidate_tasks: Vec<String> = Vec::new();

    for i in (1..=config.lookback_days).rev() {
        let day = config.date - Duration::days(i);
        let note_path = daily_dir.join(format!("{}.md", day.format("%Y-%m-%d")));

        if !note_path.exists() {
            continue;
        }

        source_days.push(day);
        let content = fs::read_to_string(&note_path)
            .map_err(|e| format!("Failed to read {}: {e}", note_path.display()))?;
        let parsed = parse_daily_note(&content);

        completed.extend(parsed.completed);
        decisions.extend(parsed.decisions);
        blockers.extend(parsed.blockers);
        questions.extend(parsed.questions);
        candidate_tasks.extend(parsed.candidate_tasks);
    }

    if source_days.is_empty() {
        return Err(
            "No source daily notes found. Create at least one note in 40_work_tracking/daily/YYYY-MM-DD.md before running.".to_string(),
        );
    }

    completed = dedupe_preserve(completed);
    decisions = dedupe_preserve(decisions);
    blockers = dedupe_preserve(blockers);
    questions = dedupe_preserve(questions);
    candidate_tasks = dedupe_preserve(candidate_tasks);

    let source_labels = source_days
        .iter()
        .map(|d| d.format("%Y-%m-%d").to_string())
        .collect::<Vec<_>>()
        .join(", ");

    let summary_path = summaries_dir.join(format!("{}-summary.md", config.date.format("%Y-%m-%d")));
    let summary = format!(
        "# {} Next-Day Summary\n\nSource notes: {}\n\n## Completed Work Highlights\n{}\n## Key Decisions\n{}\n## Risks / Blockers\n{}\n## Open Questions\n{}",
        config.date.format("%Y-%m-%d"),
        source_labels,
        markdown_bullets(&completed, "No completed work bullets detected."),
        markdown_bullets(&decisions, "No explicit decision bullets detected."),
        markdown_bullets(&blockers, "No blockers captured."),
        markdown_bullets(&questions, "No open questions captured.")
    );

    write_file(&summary_path, &summary)?;

    let mut priority = candidate_tasks;
    priority.extend(blockers.iter().map(|b| format!("Resolve blocker: {b}")));
    priority.extend(questions.iter().map(|q| format!("Answer question: {q}")));
    let priority = dedupe_preserve(priority);

    let tasks_path = tasks_dir.join(format!("{}-tasks.md", config.date.format("%Y-%m-%d")));
    let tasks = format!(
        "# {} Task Draft\n\n## Priority Tasks\n{}\n## Notes\n- Adjust ordering and scope before execution.\n",
        config.date.format("%Y-%m-%d"),
        markdown_task_bullets(&priority, "Add tasks based on current priorities.")
    );

    write_file(&tasks_path, &tasks)?;

    let summary_rel = summary_path
        .strip_prefix(&root)
        .map_err(|e| format!("Failed to compute output path: {e}"))?;
    let tasks_rel = tasks_path
        .strip_prefix(&root)
        .map_err(|e| format!("Failed to compute output path: {e}"))?;

    println!("Generated: {}", summary_rel.display());
    println!("Generated: {}", tasks_rel.display());

    Ok(())
}

fn main() {
    match parse_args().and_then(run) {
        Ok(()) => {}
        Err(msg) => {
            eprintln!("{msg}");
            std::process::exit(1);
        }
    }
}
