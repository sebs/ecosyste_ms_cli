# Interesting Ecosystems CLI Combinations

These shell scripts demonstrate creative ways to combine the ecosyste.ms APIs using the CLI and jq.

## 1. Security Audit Pipeline
Find all packages your organization depends on and check for security advisories.
```bash
#!/bin/bash
# security-audit.sh - Audit all dependencies for security issues
ORG="your-org"
echo "# Security Audit for $ORG"
echo "Generated: $(date)"
echo

# Get all repos for the org
ecosystems repos hosts github-owners "$ORG" -o json | jq -r '.[] | .full_name' | while read repo; do
    echo "## Checking $repo"
    # Get dependencies from the repo
    ecosystems repos lookup "https://github.com/$repo" -o json | jq -r '.dependencies[]?.package_name' | sort | uniq | while read pkg; do
        # Check each package for advisories
        advisories=$(ecosystems packages lookup-name "$pkg" -o json | jq '.advisories // []')
        if [ "$advisories" != "[]" ]; then
            echo "⚠️  $pkg has security advisories:"
            echo "$advisories" | jq -r '.[] | "   - \(.severity // "unknown"): \(.title)"'
        fi
    done
    echo
done
```

## 2. Technology Stack Analyzer
Analyze what technologies are used together by looking at awesome lists and their projects.
```bash
#!/bin/bash
# tech-stack-analyzer.sh - Find common technology combinations
TOPIC="$1"
echo "# Technology Stack Analysis: $TOPIC"

# Get projects from awesome lists for the topic
ecosystems awesome lists -o json | jq -r --arg topic "$TOPIC" '.[] | select(.topics[]? | contains($topic)) | .name' | head -10 | while read list; do
    echo "## From awesome-$list"
    # Get projects from this list and analyze their dependencies
    ecosystems awesome projects --list "$list" -o json | jq -r '.[].repository_url' | head -5 | while read repo_url; do
        if [[ -n "$repo_url" ]]; then
            # Get summary of the project
            summary=$(ecosystems summary project-lookup "$repo_url" -o json 2>/dev/null)
            if [[ -n "$summary" ]]; then
                echo "### $(echo "$summary" | jq -r '.name // "Unknown"')"
                echo "Languages: $(echo "$summary" | jq -r '.repository.languages // {} | keys | join(", ")')"
                echo "Key Dependencies: $(echo "$summary" | jq -r '.packages[0].dependencies // [] | .[0:5] | .[].package_name' | tr '\n' ', ' | sed 's/,$//')"
                echo
            fi
        fi
    done
done
```

## 3. Package Impact Analyzer
Find the blast radius of a package by analyzing its dependents across ecosystems.
```bash
#!/bin/bash
# package-impact.sh - Analyze the impact of a package across ecosystems
PACKAGE="$1"
ECOSYSTEM="${2:-npm}"

echo "# Impact Analysis for $PACKAGE ($ECOSYSTEM)"
echo "Generated: $(date)"
echo

# Get package info
pkg_info=$(ecosystems packages registry-package "$ECOSYSTEM" "$PACKAGE" -o json)
echo "## Package Overview"
echo "- Latest Version: $(echo "$pkg_info" | jq -r '.latest_release_number')"
echo "- Downloads: $(echo "$pkg_info" | jq -r '.downloads // "N/A"')"
echo "- Dependents Count: $(echo "$pkg_info" | jq -r '.dependents_count // 0')"
echo

# Get top dependents
echo "## Top Dependents (by downloads)"
ecosystems packages package-dependents "$ECOSYSTEM" "$PACKAGE" --limit 10 -o json | jq -r '.[] | "- \(.name): \(.downloads // 0) downloads"'

# Find which major projects use this
echo
echo "## Used by Notable Projects"
ecosystems repos package-usage "$ECOSYSTEM" "$PACKAGE" --limit 20 -o json | jq -r '.[] | select(.stars > 100) | "- [\(.full_name)](\(.html_url)) (⭐ \(.stars))"' | sort -t'⭐' -k2 -nr
```

## 4. Maintainer Portfolio Explorer
Discover all projects and packages maintained by a specific person.
```bash
#!/bin/bash
# maintainer-portfolio.sh - Build a complete portfolio for a maintainer
MAINTAINER="$1"

echo "# Portfolio: $MAINTAINER"
echo

# Find packages across registries
for registry in npm pypi rubygems packagist cargo; do
    echo "## $registry packages"
    result=$(ecosystems packages registry-maintainer "$registry" "$MAINTAINER" -o json 2>/dev/null)
    if [[ "$?" -eq 0 ]] && [[ "$result" != "[]" ]]; then
        echo "$result" | jq -r '.[] | "- [\(.name)](\(.homepage // .repository_url // "#")) - \(.description // "No description")"' | head -10
    else
        echo "No packages found"
    fi
    echo
done

# Find GitHub repositories
echo "## GitHub Repositories"
ecosystems repos hosts github-owners "$MAINTAINER" -o json 2>/dev/null | jq -r '.[] | "- [\(.full_name)](\(.html_url)) - ⭐ \(.stargazers_count) - \(.description // "No description")"' | head -10
```

## 5. License Compatibility Checker
Check if all dependencies of a project have compatible licenses.
```bash
#!/bin/bash
# license-checker.sh - Check license compatibility in dependency tree
REPO_URL="$1"
ALLOWED_LICENSES="MIT|Apache-2.0|BSD-3-Clause|BSD-2-Clause|ISC"

echo "# License Compatibility Check"
echo "Repository: $REPO_URL"
echo "Allowed: $ALLOWED_LICENSES"
echo

# Get project summary
summary=$(ecosystems summary project-lookup "$REPO_URL" -o json)
project_license=$(echo "$summary" | jq -r '.repository.license // "Unknown"')
echo "Project License: $project_license"
echo

# Check all dependencies
echo "## Dependency Licenses"
echo "$summary" | jq -r '.packages[].dependencies[]' | while read -r dep; do
    name=$(echo "$dep" | jq -r '.package_name')
    ecosystem=$(echo "$dep" | jq -r '.ecosystem')

    # Get package license
    pkg_info=$(ecosystems packages registry-package "$ecosystem" "$name" -o json 2>/dev/null)
    license=$(echo "$pkg_info" | jq -r '.licenses // "Unknown"')

    if [[ ! "$license" =~ $ALLOWED_LICENSES ]] && [[ "$license" != "Unknown" ]]; then
        echo "⚠️  $name ($ecosystem): $license - INCOMPATIBLE"
    else
        echo "✅ $name ($ecosystem): $license"
    fi
done | sort | uniq
```

## 6. Ecosystem Health Dashboard
Generate a health report for a specific technology ecosystem.
```bash
#!/bin/bash
# ecosystem-health.sh - Analyze health of packages in an ecosystem
TOPIC="$1"
LIMIT="${2:-20}"

echo "# Ecosystem Health Report: $TOPIC"
echo "Generated: $(date)"
echo

# Get top packages for the topic
ecosystems packages search --keywords "$TOPIC" --limit "$LIMIT" -o json | jq -r '.[]' | while read -r pkg_json; do
    name=$(echo "$pkg_json" | jq -r '.name')
    ecosystem=$(echo "$pkg_json" | jq -r '.ecosystem')

    # Get detailed info
    details=$(ecosystems packages registry-package "$ecosystem" "$name" -o json 2>/dev/null)

    # Calculate health score (simple example)
    stars=$(echo "$details" | jq -r '.stars // 0')
    dependents=$(echo "$details" | jq -r '.dependents_count // 0')
    days_since_update=$(echo "$details" | jq -r '.latest_release_published_at // "" | if . == "" then 9999 else (now - (. | fromdateiso8601)) / 86400 | floor end')

    # Simple health scoring
    if (( days_since_update < 30 )); then
        activity="🟢"
    elif (( days_since_update < 180 )); then
        activity="🟡"
    else
        activity="🔴"
    fi

    echo "- $name: $activity Activity | ⭐ $stars | 📦 $dependents dependents"
done
```

## 7. Trending Technology Discoverer
Find trending technologies by analyzing recently updated awesome lists and their new additions.
```bash
#!/bin/bash
# trending-tech.sh - Discover trending technologies from awesome lists
DAYS="${1:-30}"

echo "# Trending Technologies (Last $DAYS days)"
echo

# Get recently updated awesome lists
cutoff_date=$(date -d "$DAYS days ago" +%Y-%m-%d)

ecosystems awesome lists -o json | jq -r --arg cutoff "$cutoff_date" '.[] | select(.last_synced_at > $cutoff) | .name' | while read list; do
    echo "## From awesome-$list"

    # Get projects and check their creation/addition dates
    ecosystems awesome projects --list "$list" -o json | jq -r --arg cutoff "$cutoff_date" '.[] | select(.created_at > $cutoff) | .name // .repository_url' | head -5 | while read project; do
        if [[ -n "$project" ]]; then
            echo "- 🆕 $project"
        fi
    done
    echo
done

# Also check for trending topics
echo "## Trending Topics"
ecosystems repos topics -o json | jq -r '.[] | select(.repositories_count > 100) | "\(.name): \(.repositories_count) repos"' | sort -t':' -k2 -nr | head -10
```

## 8. Dependency Tree Visualizer
Create a visual representation of a package's dependency tree.
```bash
#!/bin/bash
# dep-tree.sh - Visualize dependency tree
ECOSYSTEM="$1"
PACKAGE="$2"
MAX_DEPTH="${3:-3}"

echo "# Dependency Tree: $PACKAGE ($ECOSYSTEM)"
echo '```mermaid'
echo 'graph TD'

# Function to get dependencies recursively
get_deps() {
    local pkg="$1"
    local depth="$2"
    local parent="$3"

    if (( depth >= MAX_DEPTH )); then
        return
    fi

    # Get dependencies
    ecosystems packages registry-package "$ECOSYSTEM" "$pkg" -o json 2>/dev/null | jq -r '.dependencies[]?.package_name' | while read dep; do
        if [[ -n "$dep" ]]; then
            # Create safe node names
            safe_parent=$(echo "$parent" | tr -d '@/.-' | tr '[:lower:]' '[:upper:]')
            safe_dep=$(echo "$dep" | tr -d '@/.-' | tr '[:lower:]' '[:upper:]')

            echo "    $safe_parent[$parent] --> $safe_dep[$dep]"

            # Recurse
            get_deps "$dep" $((depth + 1)) "$dep"
        fi
    done | sort | uniq
}

# Start with root package
get_deps "$PACKAGE" 0 "$PACKAGE"

echo '```'
```

## 9. Cross-Ecosystem Package Finder
Find packages that exist across multiple ecosystems (e.g., both npm and pypi).
```bash
#!/bin/bash
# cross-ecosystem.sh - Find packages that exist in multiple ecosystems
KEYWORD="$1"

echo "# Cross-Ecosystem Packages: $KEYWORD"
echo

declare -A packages

# Search across ecosystems
for ecosystem in npm pypi rubygems packagist cargo; do
    echo "Searching $ecosystem..." >&2
    ecosystems packages search --keywords "$KEYWORD" --ecosystem "$ecosystem" --limit 50 -o json 2>/dev/null | jq -r '.[] | .name' | while read name; do
        # Normalize name (remove ecosystem-specific prefixes)
        normalized=$(echo "$name" | sed 's/^@[^/]*\///' | tr '[:upper:]' '[:lower:]')
        packages["$normalized"]+="$ecosystem "
    done
done

# Find packages in multiple ecosystems
echo "## Packages in Multiple Ecosystems"
for pkg in "${!packages[@]}"; do
    ecosystems=$(echo "${packages[$pkg]}" | tr ' ' '\n' | sort | uniq | tr '\n' ' ')
    count=$(echo "$ecosystems" | wc -w)
    if (( count > 1 )); then
        echo "- **$pkg**: $ecosystems"
    fi
done | sort
```

## 10. Project Sustainability Scorer
Calculate a sustainability score for open source projects based on multiple factors.
```bash
#!/bin/bash
# sustainability-scorer.sh - Score project sustainability
REPO_URL="$1"

echo "# Sustainability Score: $REPO_URL"
echo

# Get comprehensive project data
summary=$(ecosystems summary project-lookup "$REPO_URL" -o json)
repo_data=$(echo "$summary" | jq '.repository')
packages=$(echo "$summary" | jq '.packages[]' | head -1)

# Calculate various metrics
score=0
max_score=0

# 1. Activity (max 20 points)
days_since_commit=$(echo "$repo_data" | jq -r '.pushed_at // "" | if . == "" then 365 else (now - (. | fromdateiso8601)) / 86400 | floor end')
if (( days_since_commit < 30 )); then
    score=$((score + 20))
elif (( days_since_commit < 90 )); then
    score=$((score + 10))
elif (( days_since_commit < 180 )); then
    score=$((score + 5))
fi
max_score=$((max_score + 20))
echo "✓ Activity: $days_since_commit days since last commit"

# 2. Community (max 20 points)
contributors=$(echo "$repo_data" | jq -r '.contributors_count // 1')
if (( contributors > 50 )); then
    score=$((score + 20))
elif (( contributors > 10 )); then
    score=$((score + 15))
elif (( contributors > 3 )); then
    score=$((score + 10))
else
    score=$((score + 5))
fi
max_score=$((max_score + 20))
echo "✓ Contributors: $contributors"

# 3. Popularity (max 20 points)
stars=$(echo "$repo_data" | jq -r '.stargazers_count // 0')
if (( stars > 1000 )); then
    score=$((score + 20))
elif (( stars > 100 )); then
    score=$((score + 15))
elif (( stars > 10 )); then
    score=$((score + 10))
fi
max_score=$((max_score + 20))
echo "✓ Stars: $stars"

# 4. Dependencies health (max 20 points)
if [[ -n "$packages" ]]; then
    dep_count=$(echo "$packages" | jq -r '.dependencies | length')
    if (( dep_count < 10 )); then
        score=$((score + 20))
    elif (( dep_count < 50 )); then
        score=$((score + 15))
    elif (( dep_count < 100 )); then
        score=$((score + 10))
    fi
    echo "✓ Dependencies: $dep_count"
else
    dep_count=0
fi
max_score=$((max_score + 20))

# 5. Documentation (max 20 points)
has_readme=$(echo "$repo_data" | jq -r '.readme_name // "" | if . != "" then 1 else 0 end')
has_license=$(echo "$repo_data" | jq -r '.license // "" | if . != "" then 1 else 0 end')
doc_score=$((has_readme * 10 + has_license * 10))
score=$((score + doc_score))
max_score=$((max_score + 20))
echo "✓ Documentation: README=$has_readme, LICENSE=$has_license"

# Calculate percentage
percentage=$((score * 100 / max_score))

echo
echo "## Final Score: $score/$max_score ($percentage%)"

# Grade
if (( percentage >= 80 )); then
    echo "Grade: A - Highly Sustainable ✅"
elif (( percentage >= 60 )); then
    echo "Grade: B - Moderately Sustainable 👍"
elif (( percentage >= 40 )); then
    echo "Grade: C - Needs Improvement ⚠️"
else
    echo "Grade: D - At Risk ❌"
fi
```

## Usage Tips

1. Make all scripts executable: `chmod +x *.sh`
2. Most scripts accept parameters - check the first few lines for usage
3. Combine scripts using pipes for more complex analysis
4. Use `--limit` and pagination options to handle large datasets
5. Export results to files using output redirection
6. Consider caching results for expensive operations

## Example Combinations

```bash
# Find vulnerable dependencies in trending projects
./trending-tech.sh 7 | grep "🆕" | cut -d' ' -f3 | xargs -I {} ./security-audit.sh {}

# Build a portfolio of top maintainers in an ecosystem
ecosystems packages search --ecosystem npm --limit 100 -o json | \
  jq -r '.[] | .maintainers[]' | sort | uniq -c | sort -nr | \
  head -10 | awk '{print $2}' | xargs -I {} ./maintainer-portfolio.sh {}

# Analyze sustainability of all projects in an awesome list
ecosystems awesome projects --list react -o json | \
  jq -r '.[].repository_url' | xargs -I {} ./sustainability-scorer.sh {}
```
