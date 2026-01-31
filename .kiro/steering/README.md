# Steering Files

## What Are Steering Files?

Steering files are **project-wide context and guidelines** that Kiro automatically includes when working on your code. They ensure consistency, quality, and adherence to your team's standards across all development work.

Think of them as:
- **Living documentation** that guides development
- **Automated code review** that happens before code is written
- **Team knowledge** captured in a reusable format

## Steering Files in This Project

### 1. architecture-patterns.md
**Inclusion**: Always included

**Purpose**: Defines the Modified MVC architecture pattern used throughout the project

**Key Topics**:
- Layer responsibilities (Models, Views, Controllers)
- Dependency rules (what can import what)
- Data flow patterns
- State management
- Immutability guidelines
- Anti-patterns to avoid

**When to reference**: When creating new modules, refactoring code, or making architectural decisions

---

### 2. python-standards.md
**Inclusion**: Always included

**Purpose**: Python coding standards and conventions for the project

**Key Topics**:
- PEP 8 compliance and formatting
- Naming conventions (classes, functions, constants)
- Type hints requirements
- Documentation standards (docstrings)
- Import organization
- Error handling patterns
- Code organization

**When to reference**: When writing any Python code

---

### 3. testing-practices.md
**Inclusion**: Always included

**Purpose**: Comprehensive testing guidelines for unit and property-based tests

**Key Topics**:
- Testing philosophy (what to test, what not to test)
- Test organization and structure
- Unit testing with pytest
- Property-based testing with Hypothesis
- Custom test strategies
- Test isolation and mocking
- Coverage goals
- Debugging failed tests

**When to reference**: When writing tests, debugging test failures, or planning test coverage

---

### 4. pygame-patterns.md
**Inclusion**: Conditional (when Python files are read)

**Purpose**: Pygame-specific patterns and best practices

**Key Topics**:
- Pygame initialization sequence
- Game loop structure
- Event handling patterns
- Rendering order and best practices
- Text and color management
- Coordinate system conversions
- Performance optimization
- Common Pygame pitfalls

**When to reference**: When working with Pygame code (views/, main.py)

---

### 5. project-context.md
**Inclusion**: Always included

**Purpose**: High-level project context, goals, and workflow

**Key Topics**:
- Project overview and goals
- Technology stack and rationale
- Development workflow (spec-driven approach)
- Project structure
- Development principles
- Common patterns in this project
- Expected challenges and solutions
- Success criteria

**When to reference**: When starting work, onboarding, or making high-level decisions

---

## How Steering Files Work

### Automatic Inclusion
When you ask Kiro to implement a task or write code, it automatically:
1. Reads the spec files (requirements, design, tasks)
2. Loads relevant steering files based on inclusion rules
3. Uses all this context to write code that follows your standards

### Inclusion Types

**Always Included** (default):
```markdown
---
inclusion: always
---
```
These files are included in every interaction.

**Conditional Inclusion** (file pattern matching):
```markdown
---
inclusion: fileMatch
fileMatchPattern: '**/*.py'
---
```
These files are included only when specific files are being worked on.

**Manual Inclusion** (user-triggered):
```markdown
---
inclusion: manual
---
```
These files are included only when you explicitly reference them with #context.

### Current Configuration
- **Always included**: architecture-patterns.md, python-standards.md, testing-practices.md, project-context.md
- **Conditional**: pygame-patterns.md (when working with Python files)
- **Manual**: None currently

## Benefits of Steering Files

### Consistency
- All code follows the same patterns
- No need to remember every guideline
- New team members get up to speed faster

### Quality
- Standards are enforced automatically
- Best practices are built-in
- Common mistakes are prevented

### Documentation
- Guidelines are documented and versioned
- Easy to update as project evolves
- Serves as reference for the team

### Efficiency
- No need to repeat guidelines in every conversation
- Kiro knows your preferences automatically
- Focus on the problem, not the process

## Maintaining Steering Files

### When to Update
- **New patterns emerge**: Document successful patterns you discover
- **Standards change**: Update when team agrees on new conventions
- **Lessons learned**: Add guidance based on bugs or issues encountered
- **Technology changes**: Update when upgrading libraries or tools

### How to Update
1. Edit the relevant steering file in `.kiro/steering/`
2. Changes take effect immediately (no restart needed)
3. Consider adding a changelog entry in the file
4. Communicate changes to the team

### Example Update
If you discover a better way to handle Pygame events:
1. Open `pygame-patterns.md`
2. Update the "Event Handling" section
3. Add a note about why the change was made
4. Save the file

## Creating New Steering Files

### When to Create New Files
- **New technology**: Adding a new library or framework
- **New domain**: Working on a new area (e.g., database, API)
- **Team growth**: Documenting tribal knowledge
- **Complexity**: When verbal guidelines become too complex

### Template for New Steering Files
```markdown
---
inclusion: always  # or fileMatch, or manual
---

# [Title]

## Overview
Brief description of what this file covers and why it exists.

## [Section 1]
Content...

## [Section 2]
Content...

## Checklist
- [ ] Item 1
- [ ] Item 2
```

### Example: Adding Database Guidelines
If you later add a database to the project:
1. Create `.kiro/steering/database-patterns.md`
2. Document connection management, query patterns, migrations
3. Set inclusion to `fileMatch` with pattern `**/models/*.py`
4. Kiro will automatically use it when working with database code

## Steering Files vs Specs

### Key Differences

**Steering Files** (`.kiro/steering/`):
- **Scope**: Project-wide
- **Purpose**: HOW to build (standards, patterns)
- **Lifetime**: Long-lived, evolve slowly
- **Examples**: Coding standards, architecture patterns

**Spec Files** (`.kiro/specs/`):
- **Scope**: Feature-specific
- **Purpose**: WHAT to build (requirements, design)
- **Lifetime**: Created per feature, completed when feature is done
- **Examples**: User authentication spec, payment processing spec

### They Work Together
When implementing a task:
1. **Spec** tells Kiro WHAT to build (requirements, design, specific task)
2. **Steering** tells Kiro HOW to build it (standards, patterns, best practices)
3. **Result**: Code that meets requirements AND follows standards

## Tips for Effective Steering Files

### Do's
✅ Be specific and actionable
✅ Include examples (good and bad)
✅ Explain the "why" behind guidelines
✅ Keep files focused (one topic per file)
✅ Update based on real experience
✅ Use checklists for verification

### Don'ts
❌ Don't make files too long (split if needed)
❌ Don't include outdated information
❌ Don't be overly prescriptive (allow flexibility)
❌ Don't duplicate information across files
❌ Don't include project-specific code (that goes in specs)

## Getting Help

### If Guidelines Conflict
If steering files seem to contradict each other:
1. Check if one is more specific (specific wins)
2. Consider the context (which applies to current work?)
3. Update files to clarify the conflict
4. Ask the team for consensus

### If Guidelines Are Unclear
If a guideline is confusing:
1. Ask Kiro to explain the guideline
2. Look at examples in the codebase
3. Propose a clarification
4. Update the steering file

### If You Disagree with a Guideline
If you think a guideline should change:
1. Document why (what problem does it cause?)
2. Propose an alternative
3. Discuss with the team
4. Update the steering file if agreed

## Summary

Steering files are your project's **automated knowledge base**. They ensure that:
- Every piece of code follows the same standards
- Best practices are consistently applied
- New team members can contribute effectively
- Quality is maintained as the project grows

For this Tetris project, the steering files capture:
- **Architecture**: How components are organized
- **Python standards**: How to write Python code
- **Testing**: How to verify correctness
- **Pygame patterns**: How to use Pygame effectively
- **Project context**: What we're building and why

As you work through the implementation, these files will guide every decision, ensuring a high-quality, maintainable codebase.
