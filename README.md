# Operating Systems Projects

This repository is a professional systems-focused collection that strengthens operating systems fundamentals through hands-on implementation, practical computing exercises, and selected BS AI coursework context.

## Table of Contents

- [Overview](#overview)
- [Business Goals](#business-goals)
- [Technology Stack](#technology-stack)
- [How to Use This Repository](#how-to-use-this-repository)
- [Repository Guidelines](#repository-guidelines)
- [Code Guidelines](#code-guidelines)
- [Future Direction](#future-direction)

## Overview

The repository focuses on process behavior, synchronization, resource control, and low-level system reasoning relevant to robust software engineering.

## Business Goals

- Improve software reliability with stronger systems understanding.
- Support performance-aware technical decisions for backend infrastructure.
- Build practical foundations for secure and efficient computing designs.
- Strengthen engineering judgment for concurrency and resource-sensitive workloads.

## Projects

| Project | Language | OS Concepts |
|---|---|---|
| [Critical Section Problem](Critical%20Section%20Problem/) | C | Race conditions, mutex (`pthread_mutex_t`) |
| [Peterson's Solution for Synchronization and Concurrency](Petersons%20Solution%20for%20Synchronization%20and%20Concurrency/) | Python | Mutual exclusion, Peterson's algorithm |
| [Concurrent Banking System with OS Scheduling](Concurrent%20Banking%20System%20with%20OS%20Scheduling/) | Python | Mutex, semaphore, threads, IPC, Round Robin scheduling |

## Technology Stack

- Languages: C, Python (project dependent)
- Core topics: concurrency, scheduling, synchronization, IPC, memory/resource management
- Tooling: GCC/G++, Python 3.8+, VS Code/Visual Studio
- Workflow: Git/GitHub and implementation-first iteration

## How to Use This Repository

1. Select a project folder based on the OS concept you want to study.
2. Review local instructions or compiler requirements.
3. Build with the expected toolchain for that project.
4. Run and validate behavior against expected synchronization/scheduling outcomes.

## Repository Guidelines

- Keep projects concept-focused and implementation-oriented.
- Document assumptions, execution steps, and expected behavior.
- Keep each project runnable with minimal external dependencies.
- Add concise notes for algorithm or concurrency design choices.

## Code Guidelines

- Make thread/process coordination logic explicit and readable.
- Prefer deterministic test scenarios where possible.
- Avoid hidden shared state and document synchronization primitives used.
- Keep error handling clear for system calls and boundary conditions.

## Future Direction

This repository will continue to grow with deeper scheduling simulations, memory strategy work, file-system concepts, and performance-focused systems experiments.
