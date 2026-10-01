<!--
POSITIONING ARCHIVE ONLY — not evidence for v6.

This Russian-language file is a retained strategic/positioning source used for
Motivation, Scope, rival architecture, and research-programme map in the English
preprint. Do not treat it as empirical support for matched-channel claims, as a
replacement for Nelson et al. (2010), or as a hierarchical v9 result.
Local/internal path references inside the text are historical and not public deliverables.
-->

# Исследование: FEP / Active Inference как кандидат на фундаментальный прорыв

Протокол: Scientific Research Agent Protocol v2.0
Дата: 2026-09-28
Вход: гипотеза пользователя (файл «На основе анализа ко.txt») о том, что Принцип свободной энергии (FEP) и Активное выведение (Active Inference) в каузально-генеративной формулировке являются наиболее сильной объединяющей гипотезой; заявлена числовая уверенность 0.85; предложен решающий эксперимент (зарегистрированный closed-loop тест против Bayes-RL/PID/MPC).

---

## 1. Executive Summary

1. **F-001 (supported):** FEP как общий принцип широко (включая сторонников) рассматривается как формально нефальсифицируемая тавтология; научный вопрос — не «верен ли принцип», а «порождает ли он специфические, проверяемые модели». Статус: supported.
2. **F-002 (supported):** Алгоритмы active inference конкурентоспособны с RL на стандартных бенчмарках, но «решающего» зарегистрированного closed-loop эксперимента с заблаговременными количественными предсказаниями против Bayes-RL/PID/MPC не обнаружено. Статус: supported (по состоянию поиска).
3. **F-003 (plausible):** Каузально-генеративная формулировка (closed-loop, causal system identification) — правильно идентифицированное узкое место; она переводит дискуссию из философии в экспериментальную плоскость. Статус: plausible (оценка).
4. **F-004 (weak):** Единственный найденный экспериментальный успех раннего предсказания: тиоридазин вызывает анатомические дефекты у Xenopus laevis, как предсказано моделью (одиночный результат, требует репликации). Статус: weak.
5. **F-005 (supported):** Заявленная уверенность «0.85» и «первое место» в корпусе не имеют методологического основания — это ложная точность (инвариант Calibration); корпус-источник не предоставлен. Статус: contradicted как числовая оценка.
6. **F-006 (supported):** Проблема масштабирования (coarse-graining марковских одеял) открыта; новые формулировки FEP уже отказались от предпосылок постоянного марковского одеяла и NESS. Статус: supported.
7. **F-007 (plausible):** Конкурирующее объяснение №1: вся инженерная ценность active inference объяснима без физических претензий FEP (EFE-цели как вариант intrinsic motivation / exploration bonuses в RL). Если подтвердится, «прорыв» будет принадлежать алгоритмам, а не принципу.

## 2. Research Environment Passport

```yaml
research_mode: exploratory
evidence_state: conflicting
error_cost: medium        # исследовательская задача; клинические приложения — high
evidence_freshness: recent_required
empirical_validation: partially_available
reproducibility_requirement: high
methodological_complexity: high
autonomy_level: analytical
human_review_requirement: recommended  # обязательно при переходе к клиническим/AGI-выводам
```

## 3. Research Question

RQ-1: Обоснованно ли утверждение, что FEP/Active Inference в closed-loop формулировке — наиболее сильная объединяющая гипотеза с фундаментальным прорывным потенциалом?
RQ-2: Способен ли предложенный «решающий эксперимент» (зарегистрированный closed-loop с out-of-sample предсказаниями интервенций) фальсифицировать ключевые альтернативы?
RQ-3: Каков следующий наиболее информативный шаг?

Критерий успешности (измеримый): наличие/отсутствие в литературе (2020–2026) зарегистрированного эксперимента, где генеративная FEP-модель заблаговременно (до тестовых данных) дала количественные предсказания реакции системы на новые интервенции и превзошла Bayes-RL/PID/MPC в out-of-sample точности.

## 4. Domain Evidence Standard

Поле: теоретическая нейронаука / вычислительная психиатрия / ИИ-агенты (междисциплинарно).

- Первичные evidence: зарегистрированные preregistered прогнозы; воспроизводимые симуляции с открытым кодом; прямые измерения (нейрофизиология, поведенческие эксперименты); формальные доказательства.
- Иерархия claim'ов: confirmed — независимая репликация прогноза; supported — конвергенция независимых источников; plausible — единичное согласие модели и данных; weak — пост-хок объяснение.
- Стандарт причинности: темпоральность + интервенционные данные (не наблюдательная совместимость).
- Стандарт новизны: не «не найдено в моём корпусе», а отсутствие аналогов после поиска по смежной терминологии.
- Известные failure modes: redescription (пост-хок переописание), unfalsifiable generality, toy-model overreach, публикационное смещение в пользу положительных результатов.

## 5. Baseline

`<fact>` FEP (Friston) формален и доказуем при своих предпосылках (система с марковским одеялом, NESS, Langevin-динамика); при этом он сам по себе не даёт конкретных предсказаний о поведении без дополнительных предположений о генеративной модели (критика Millidge; LessWrong-анализ с ссылками на признание нефальсифицируемости самим Friston).
`<fact>` Сильная критика 2025 г. (Mangalam, «The Emperor's New Pseudo-Theory»): FEP как pseudo-theory, метаболизирующая противоречия; см. также ответные позиционные работы, пивотящие к «структурной эпистемологии».
`<fact>` Индустрия: active inference-агенты решают стандартные RL-бенчмарки; DAIF (2026) достигает результатов, конкурентных DreamerV3 на ряде задач DMC; NetAIF заявляет превосходство над DRL по эффективности и качеству.
`<fact>` Вычислительная психиатрия: precision-аккаунты объясняют smooth pursuit в шизофрении, force-matching illusion, черты аутизма; признано: преимущественно теоретические/симуляционные работы, без валидации на крупных клинических когортах.
`<fact>` Один экспериментальный тест прогноза: тиоридазин → дефекты морфогенеза Xenopus (Pezzulo et al., 2022).
`<fact>` Теоретические ослабления: новые формулировки FEP не требуют постоянного марковского одеяла и NESS (Alignment Forum, 2025).

## 6. Data, Sources and Tools

```text
AVAILABLE: файл пользователя (гипотеза); веб-поиск (scholar-grade источники: PMC, arXiv, Frontiers, OpenReview)
USED: 2 раунда поиска, 9 запросов; 16 + 14 результатов
NOT USED: первичные PDF (несколько доступны только как препринты/записи ResearchGate — качество источника понижено)
UNAVAILABLE: корпус «блокнота», на котором основана оценка 0.85 (<unknown>)
```

## 7. Methods

`<fact>` Выполнено: (1) декомпозиция гипотезы пользователя на проверяемые claim'ы; (2) два раунда целевого поиска по критике фальсифицируемости, сравнению с RL, клиническим evidence, проблеме масштабирования; (3) оценка каждого claim'а по иерархии Domain Evidence Standard; (4) построение конкурирующих гипотез и матрицы фальсификации; (5) adversarial review.
`<not_executed>` Систематический обзор (PRISMA) не выполнялся; поиск не исчерпывающий.

## 8. Key Findings

```yaml
finding:
  id: "F-001"
  observation: "FEP как принцип формально нефальсифицируем (признают и сторонники)"
  interpretation: "Научная ценность FEP определяется продуктивностью производных моделей, а не истинностью принципа; аналогия — принцип наименьшего действия"
  linked_claims: ["C-001"]
  supporting_evidence: ["E-001", "E-002"]
  evidence_against: ["E-007"]  # сторонники: принцип полезен как организующая рамка
  alternative_explanations: ["ценность — в алгоритмах, а не в принципе (H-4)"]
  confidence: "high (категориальная; конвергенция независимых источников)"

finding:
  id: "F-002"
  observation: "Решающего зарегистрированного closed-loop эксперимента по схеме пользователя не найдено"
  interpretation: "Дискриминирующий тест из гипотезы пользователя ещё не проведён — это и есть главная незакрытая ветка"
  linked_claims: ["C-002"]
  supporting_evidence: ["E-003", "E-004", "E-005"]
  evidence_against: []
  alternative_explanations: ["эксперимент существует, но не индексируется поиском — вероятность низкая, не нулевая"]
  confidence: "medium (границы поиска: 9 запросов, 2 раунда)"

finding:
  id: "F-003"
  observation: "Оценка '0.85, первое место в корпусе' не имеет калибровочного основания"
  interpretation: "Числовая уверенность без механизма калибровки — ложная точность; корпус-источник не предоставлен, воспроизводить оценку нельзя"
  linked_claims: ["C-003"]
  supporting_evidence: ["E-006"]
  evidence_against: []
  alternative_explanations: ["оценка могла быть калибрована внутри непредоставленного корпуса"]
  confidence: "high"

finding:
  id: "F-004"
  observation: "Клинические применения описываются как 'largely theoretical and simulation-based'"
  interpretation: "Претензия 'новая парадигма в медицине' — пока программа, не результат"
  linked_claims: ["C-004"]
  supporting_evidence: ["E-005", "E-008"]
  evidence_against: ["E-009"]  # один экспериментальный успех (Xenopus)
  alternative_explanations: []
  confidence: "medium"

finding:
  id: "F-005"
  observation: "Проблема coarse-graining (клетка → ткань → организм) открыта; теоремы укрупнения нет"
  interpretation: "Scale-gap — реальный теоретический риск, согласованный с исходным файлом"
  linked_claims: ["C-005"]
  supporting_evidence: ["E-010", "E-011"]
  evidence_against: []
  alternative_explanations: []
  confidence: "medium-high"
```

## 9. Competing Hypotheses

| ID | Гипотеза | Статус |
|---|---|---|
| H-1 | FEP/Active Inference (closed-loop causal) — сильнейшая объединяющая рамка; прорыв = решающий closed-loop эксперимент | active (гипотеза пользователя, скорректирована) |
| H-2 | FEP — полезный организующий принцип (как least action), научная ценность только через специфические инстанциации | active (сильный консенсус критики и части сторонников) |
| H-3 | FEP — pseudo-theory: redescription, отсутствие новых предсказаний (Mangalam 2025) | active |
| H-4 | Инженерная ценность объясняется без FEP: EFE = семейство intrinsic-motivation целей, сводимых к вариантам RL | active |
| H-5 | Клинический потенциал реален, но ограничен precision-моделями поведения (не механизмами) | weakened |

## 10. Falsification Matrix

| Hypothesis | Evidence For | Evidence Against | Falsifier | Best Discriminating Test | Status |
|---|---|---|---|---|---|
| H-1 | E-003, E-004 (конкурентные бенчмарки); E-009 (прогноз Xenopus) | E-001, E-002, E-006 | Preregistered closed-loop тест не показывает превосходства FEP-модели над Bayes-RL/PID/MPC в out-of-sample предсказаниях новых интервенций | EXP-001 | active, не проверен |
| H-2 | E-001 (Millidge: ценность = parsimony/utility), E-007 | — | FEP-инстанциации систематически уступают немодифицированным predictive processing моделям при равной сложности | EXP-001 + EXP-002 | active |
| H-3 | E-002 (Mangalam 2025) | E-009 (редкий, но реальный прогноз) | Повторяющиеся заблаговременные количественные прогнозы новых явлений из FEP-моделей | EXP-001, репликация E-009 | active |
| H-4 | E-003 (RL-эквивалентности в литературе) | — | EFE-агенты показывают устойчивое превосходство там, где RL с exploration bonuses структурно не может его достичь | EXP-001 (с контролем «RL + бонусы») | active |
| H-5 | E-005, E-008 | E-009 | Отсутствие репликации precision-прогнозов на когортах | EXP-003 | weakened |

## 11. Claim Ledger

```yaml
- id: "C-001"
  statement: "FEP как общий принцип нефальсифицируем; научная ценность — в производных моделях"
  type: theoretical
  status: supported
  evidence_for: ["E-001", "E-002"]
  evidence_against: ["E-007"]
  confidence: {category: high, numerical_probability: null, calibration_basis: null}

- id: "C-002"
  statement: "Решающий closed-loop эксперимент (по схеме пользователя) в литературе не обнаружен"
  type: descriptive
  status: supported
  evidence_for: ["E-003", "E-004", "E-005"]
  uncertainty: "поиск ограничен 9 запросами; возможны непроиндексированные препринты"
  confidence: {category: medium, numerical_probability: null, calibration_basis: null}

- id: "C-003"
  statement: "Оценка уверенности 0.85 и 'первое место' обоснованы"
  type: statistical
  status: contradicted
  evidence_for: []
  evidence_against: ["E-006"]
  confidence: {category: high}

- id: "C-004"
  statement: "FEP даёт новую парадигму в медицине/психиатрии"
  type: predictive
  status: plausible
  evidence_for: ["E-005", "E-009"]
  evidence_against: ["E-008"]
  confidence: {category: low}

- id: "C-005"
  statement: "Scale-gap (coarse-graining марковских одеял) — открытая проблема"
  type: theoretical
  status: supported
  evidence_for: ["E-010", "E-011"]
  confidence: {category: medium}
```

## 12. Evidence Ledger

```yaml
- id: "E-001"
  source: "Millidge, 'Thoughts on the Falsifiability of the Free Energy Principle' (2020)"
  type: literature
  primary_or_secondary: secondary
  quality: high
  limitations: ["блог, но автор — исследователь FEP; аргументы формальные"]

- id: "E-002"
  source: "Mangalam, 'The Emperor's New Pseudo-Theory' (OSF preprint, 2025)"
  type: literature
  primary_or_secondary: primary
  quality: medium
  limitations: ["препринт, без рецензии; сатирический тон; но аргументы ссылаются на конкретные работы"]

- id: "E-003"
  source: "Distributional Active Inference, arXiv:2601.20985 (2026)"
  type: literature
  quality: medium
  limitations: ["собственные результаты авторов метода; нет независимой репликации"]

- id: "E-004"
  source: "Network-based Active Inference (NetAIF), OpenReview"
  type: literature
  quality: low-medium
  limitations: ["заявление авторов о превосходстве над DRL"]

- id: "E-005"
  source: "Pezzulo et al., 'Active inference, morphogenesis, and computational psychiatry' (Frontiers, 2022)"
  type: literature
  quality: high
  limitations: ["обзорная часть по психиатрии опирается на симуляции"]

- id: "E-006"
  source: "файл пользователя"
  type: literature
  quality: low
  limitations: ["корпус не предоставлен; числовая оценка без калибровки"]

- id: "E-007"
  source: "'Good Science and Questionable Philosophy in a GUT' (PMC, 2021) и обсуждения сторонников"
  type: literature
  quality: medium

- id: "E-008"
  source: "Active Inference Institute, раздел Neuroscience (2026)"
  type: database
  quality: medium
  limitations: ["институциональный ресурс со стороны FEP-сообщества; признание 'clinical evidence still early' — информативно именно как самоограничение"]

- id: "E-009"
  source: "Pezzulo et al. 2022 — эксперимент с тиоридазином на Xenopus"
  type: experimental
  quality: medium
  limitations: ["единичный эксперимент; без независимой репликации"]

- id: "E-010"
  source: "Alignment Forum, 'Free Energy Principle' (обновл. 2025)"
  type: database
  quality: medium

- id: "E-011"
  source: "новые формулировки FEP без NESS/постоянного марковского одеяла (arXiv-линия работ)"
  type: literature
  quality: medium
```

## 13. Contradictions and Anomalies

- `<contradiction>` Противоречие уровня поля: «FEP объясняет всё» vs «FEP не предсказывает ничего конкретного». Разрешается различением уровней (принцип vs модель), но это различие часто нарушается в самой литературе.
- `<anomaly>` Единичный успешный прогноз (E-009) при фоне массовой пост-хок литературы — статистически ожидаем при большом числе публикаций (multiple testing); не считать сигналом до репликации.
- `<anomaly>` Заявленный «первый в корпусе» статус FEP при наличии целого кластера сильных критических публикаций 2025 г. — указывает на смещённость исходного корпуса (вероятен confirmation bias отбора источников).

## 14. Negative Results Registry

```yaml
- id: "N-001"
  hypothesis: "H-1 (частично): решающий тест уже проведён кем-то"
  test: "2 раунда целевого поиска (9 запросов)"
  expected_result: "хотя бы один зарегистрированный closed-loop FEP-эксперимент с out-of-sample интервенционными прогнозами"
  observed_result: "не найдено; ближайшие: бенчмарки RL (без интервенционных прогнозов) и робототехнические demo"
  interpretation: "поле находится ровно в точке, описанной пользователем: redescription преобладает, decisive test не проведён"
  consequence: "hypothesis weakened (версия 'уже сделано') | подтверждён тезис файла о 'узком месте'"
```

## 15. Statistical Assessment

Применимо частично. Поисковый охват: 30 результатов, 2 раунда; это не систематический обзор, coverage-оценка не определена. Power анализа неприменим. Ограничение: вероятность пропуска непроиндексированных препринтов средняя.

## 16. Adversarial Review

Роль: Adversarial Reviewer. Предположение: «FEP — сильнейшая гипотеза» ошибочно.

Наиболее правдоподобное обстоятельство, заставляющее ошибочный вывод выглядеть истинным:
1. **Confirmation bias отбора корпуса**: корпус «блокнота» составлен внутри FEP-дружественной среды; критические работы 2025 г. (Mangalam et al.) в такой корпус попадают редко. Это объясняет и «0.85», и «первое место» без калибровки.
2. **Redescription illusion**: благодаря гибкости вариационной математики любое поведение можно пост-хок описать как минимизацию свободной энергии — поле создаёт иллюзию объяснительной силы.
3. **Algorithm-provenance confusion**: успехи active inference-агентов в RL-бенчмарках зачитываются как поддержка FEP, тогда как по H-4 они могут быть полностью объяснены RL-эквивалентностью (confounding по происхождению результата).
4. **Selection / survivorship**: системы, «нарушающие» FEP, не существуют, чтобы быть найденными (тавтологичность условий применимости) — круговое подтверждение.
5. **Halo Fristona**: цитируемость и статус основателя смещают оценку потенциала (source dependence).

Вывод adversarial review: главный claim файла («наиболее сильная и перспективная объединяющая гипотеза») не подтверждён; подтвержден более слабый и полезный тезис — «поле созрело для решающего эксперимента, и его дизайн известен».

## 17. Assumption Log

```yaml
- id: "A-001"
  statement: "Файл пользователя — сгенерированное резюме корпуса; его оценки не являются первичными данными"
  source: user
  materiality: high
  consequence_if_false: "переоценка F-003"
  status: active
- id: "A-002"
  statement: "Полнота веб-поиска адекватна для ответа на RQ-1/RQ-2"
  source: inference
  materiality: medium
  status: active
```

## 18. Decision Log

```yaml
- id: "D-001"
  decision: "Делiverable = structured research report (глубина standard-deep); числовую уверенность не присваивать"
  trigger: "поля desired_output не заполнены"
  rationale: "протокол: Missing-but-Inferable"
- id: "D-002"
  decision: "Не проводить систематический PRISMA-обзор в рамках сессии"
  trigger: "бюджет времени; задача — оценка гипотезы, не мета-анализ"
  expected_information_gain: "низкий для RQ-1 при наличии целевых запросов"
```

## 19. Execution Summary

```text
EXECUTED: 2 раунда веб-поиска (9 запросов, 30 результатов); декомпозиция; построение гипотез/реестров; adversarial review
FAILED: —
PARTIAL: оценка литературы (поиск не исчерпывающий)
NOT EXECUTED: чтение первичных PDF; систематический обзор; количественный мета-анализ
REQUIRES EXTERNAL EXECUTION: EXP-001..003 (лабораторные/вычислительные эксперименты)
REQUIRES HUMAN EXPERIMENT: эксперименты на биологических системах
```

## 20. Reproducibility Status

`partially reproducible`. Воспроизводимы: запросы поиска, логика выводов, структура реестров. Не воспроизводимо: динамическая выдача поисковика на дату 2026-09-28; корпус «блокнота» (<unknown>).

## 21. Limitations

- Поиск не систематический; препринты без индексации могли быть пропущены.
- Часть источников — позиционные работы сторон самого спора о FEP; разделение фактов и мнений выполнено, но несовершенно.
- Оценка конкурентоспособности алгоритмов опирается на заявления авторов методов (E-003, E-004) без независимой репликации.

## 22. Unknowns

- Состав и методика корпуса «блокнота» (<unknown>) — критично для оценки «0.85».
- Существуют ли непроиндексированные зарегистрированные closed-loop эксперименты FEP (<unknown>, вероятность низкая).
- Наличие формальных теорем укрупнения в недавних arXiv-работах (<unknown> — требуется EXP-002).

## 23. Conclusions

```text
WHAT THE EVIDENCE SHOWS
- FEP как принцип нефальсифицируем (признано и сторонниками); научная ценность — в производных моделях.
- Решающего зарегистрированного closed-loop эксперимента по схеме из файла в доступной литературе нет.
- Клинические применения — преимущественно теория и симуляции; один экспериментальный прогноз (Xenopus) без репликации.
- Числовая оценка «0.85 / первое место» не имеет калибровочного основания и не воспроизводима.

WHAT THE EVIDENCE SUGGESTS
- Дизайн «решающего эксперимента» из файла корректен и совпадает с общепризнанным узким местом поля: переход от redescription к заблаговременным количественным интервенционным прогнозам.
- Инженерная ценность Active Inference реальна, но может принадлежать алгоритмам, а не «теории всего».

WHAT REMAINS SPECULATIVE
- Что FEP-модель превзойдёт Bayes-RL/PID/MPC в out-of-sample интервенционных предсказаниях.
- Клиническая программа как «новая парадигма».

WHAT HAS BEEN FALSIFIED
- Claim о доказанной «первом месте» и калиброванной уверенности 0.85.

WHAT REMAINS UNKNOWN
- Результат решающего эксперимента; теоремы coarse-graining; состав корпуса пользователя.
```

## 24. Next Best Experiments

```yaml
experiment:
  id: "EXP-001"
  question: "Превосходит ли зарегистрированная FEP-генеративная модель Bayes-RL/PID/MPC в заблаговременных out-of-sample предсказаниях реакции на новые интервенции?"
  hypotheses_tested: ["H-1", "H-3", "H-4"]
  expected_if_true: "FEP-модель статистически значимо точнее на заранее зафиксированных метриках; предсказания зафиксированы до сбора тестовых данных"
  expected_if_false: "паритет или проигрыш; или успех воспроизводится RL+exploration-bonus контролем"
  discriminating_power: high
  expected_information_gain: high
  cost: "средний (робототехническая платформа или нейронная культура in-vitro; 6–18 мес.)"
  risk: "низкий (in-silico/in-vitro)"
  kill_criteria: "terminate_if: нет превосходства после 2 независимых платформ; weaken_if: успех только на одной платформе"

experiment:
  id: "EXP-002"
  question: "Существует ли теорема coarse-graining: сохраняются ли байесовские/вариационные свойства марковских одеял при клетка → ткань → организм?"
  hypotheses_tested: ["H-1", "H-2"]
  expected_if_true: "условия укрупнения формализованы; класс систем, где FEP применим, расширен"
  expected_if_false: "применимость ограничена уровнем отдельных агентов"
  discriminating_power: medium-high
  expected_information_gain: high (теория)
  cost: "низкий-средний (математика)"
  risk: нулевой
  kill_criteria: "terminate_if: контрпример при реалистичных предпосылках"

experiment:
  id: "EXP-003"
  question: "Реплицируется ли precision-прогноз (тип тиоридазин → дефекты морфогенеза) с дозозависимостью и независимыми лабораториями?"
  hypotheses_tested: ["H-3", "H-5"]
  expected_information_gain: medium-high
  cost: средний
  risk: "низкий (модельный организм)"
  kill_criteria: "weaken_if: эффект не воспроизводится в 2 из 3 репликаций"
```

Порядок по information gain / cost: EXP-002 (высокий gain, минимальная цена) → EXP-001 (высокий gain, средняя цена) → EXP-003.

## 25. Reproducibility Bundle

- Запросы поиска: фиксированы в Execution Log (см. отчёт в сессии; 9 запросов, 2 раунда).
- Источники: список E-001…E-011 с оценками качества.
- Ограничение: артефакты поисковой выдачи не архивировались; воспроизведение по дате 2026-09-28.
