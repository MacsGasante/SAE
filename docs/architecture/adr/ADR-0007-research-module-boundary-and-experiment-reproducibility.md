# ADR-0007 — Research Module Boundary and Experiment Reproducibility

**Status:** Proposed

## Context

SAE currently provides deterministic analytical capabilities over the historical `Dataset`, including Frequency, Delay, and Probability. These capabilities describe the supplied data but do not define an experimental framework for simulations, hypothesis evaluation, statistical research, or future research-oriented algorithms.

The project roadmap identifies Research Modules as the next functional direction. Research must be introduced without weakening the existing Kernel and Analytics boundaries or turning research concerns into domain responsibilities.

Research also requires a stronger reproducibility contract than ordinary deterministic analytics. An experiment may depend on configuration, random seeds, module identity, input data, and result provenance. These concerns must be explicit so that an experimental result can be understood and reproduced independently of the research implementation details.

## Decision

SAE will introduce Research as a distinct application-level area, separate from the Kernel and from the existing Analytics layer.

The following architectural rules apply:

1. Research Modules may consume the public Kernel domain and Dataset APIs.
2. Research Modules may consume public Analytics APIs when an experiment needs existing analytical results.
3. The Kernel must not depend on Research.
4. Analytics must not depend on Research.
5. Research must not modify or redefine existing Kernel or Analytics contracts.
6. Research-specific result types are distinct from Analytics result types.
7. A research experiment is an explicit reproducible unit containing its module, input context, configuration, and execution context.
8. When randomness is used, the random seed is part of the experiment context and must be recorded.
9. Research configuration must be explicit and immutable for the duration of an experiment.
10. Research results must preserve sufficient provenance to identify the experiment inputs, configuration, module, and reproducibility context.
11. Research output must not be presented as a prediction, guarantee, or betting recommendation merely because an experiment produces a numerical result.
12. Research is not a substitute for the deterministic Analytics layer; it is a separate consumer of the established domain and analytical contracts.

The initial Research architecture therefore follows this dependency direction:

```text
Kernel
  ↑
  │
Analytics ─────────┐
  │                │
  └──────────────► Research
                       │
                       ▼
                   Research Result
```

The diagram expresses consumption rather than ownership: Research consumes established contracts and owns only research-specific concepts.

## Consequences

### Positive

- Research can evolve without contaminating the Kernel domain model.
- Existing Analytics contracts remain stable and reusable.
- Experiments become explicit, inspectable, and reproducible.
- Randomized research can be rerun from recorded execution context.
- Research results can carry provenance without changing Analytics result objects.
- Future statistical, simulation, algorithmic, and machine-learning modules have a stable architectural boundary.

### Negative

- Research introduces additional concepts and result types.
- Experiments require explicit configuration and provenance instead of relying on implicit runtime state.
- Some research implementations will require adapters when external libraries use incompatible data or result representations.

## Alternatives

### Extend Analytics with research features

Rejected. Analytics currently has a clear deterministic contract. Adding simulations, experiments, or predictive research would blur responsibilities and make the analytical layer responsible for concerns outside its scope.

### Put Research inside the Kernel

Rejected. Research concerns are not part of the domain model and would make the Kernel depend on experimental concepts and execution concerns.

### Build Research as an independent top-level application with no access to Analytics

Rejected. Research should be isolated, but it should be able to reuse established deterministic domain and analytical contracts rather than duplicating them.

### Start directly with a machine-learning framework

Rejected. The project first needs a framework for experiments, configuration, provenance, and reproducibility. Specific research technologies can be introduced later behind that boundary.

## Related Documents

- `ROADMAP.md`
- `PROJECT_STATUS.md`
- `docs/architecture/README.md`
- `specifications/analytics/analytics.md`
- `specifications/research/README.md`
- `specifications/research/experiment.md`
- `specifications/research/research-module.md`
- `specifications/research/result.md`
