# S13 frozen-v3 Figure 1: AI-prepared visual-review packet

**Status: proposal only; numeric onset extraction and authorized human
verification of the actual figure remain pending.** Local AI inspection of the
original image is described below, not a human attestation or independent
scientific approval. No clinical field disposition is proposed for promotion.

## Scope and baseline

This is preparation track 2 from [Issue #53's latest agent queue](https://github.com/aditmer/type1-diabetes-cure-research/issues/53#issuecomment-6506671471),
subject to [Issue #34](https://github.com/aditmer/type1-diabetes-cure-research/issues/34)
and the [approved October 29 closeout record](human-source-review-approved-2026-10-29.md).
The clean isolated branch was fetched and fast-forward checked against
`origin/main` before edits. Actual baseline and dispatch SHA are both
`119ab961c6021a34b544b8688a256b4ec65c422f` (merged PR #62).
Older candidate packets contain historical counts; they do not supersede this
baseline or the approved closeout record.

Only `independence.onset` for `Q3-S13`, target `lantidra-treated`, subcohort
`lantidra-pooled-all`, is in scope. All treated subjects in both pooled studies,
including repeat infusions, remain the target. No responder-only selection.
The authoritative S13 ledger remains **33 reported, 85
unreported_in_reviewed_material, 3 not_yet_extracted** out of 121 fields.
All 118 approved field objects, the original 14 protected approvals, all other
reports, trackers, rights records and primary approvals are unchanged.
`overall_followup` and `other_evidence` belong to a separate proposal owner;
this packet changes neither their schema nor any frozen rule.

## Exact source and original figure access route

Source: National Library of Medicine, DailyMed, LANTIDRA label submitted by
CellTrans Inc. The approved source is
`SPL-v3-a3163e14-0404-4e27-884b-f6f9f7f695bc`, effective **2026-01-13**,
not the current live label or a substitute FDA/manufacturer PDF.

| Object checked on 2026-10-29 | Identity |
|---|---|
| Official frozen archive | [DailyMed ZIP 940595](https://dailymed.nlm.nih.gov/dailymed/getArchivalFile.cfm?archive_id=940595) |
| ZIP | 327,121 bytes; SHA-256 `db33f66f3b6e3433d0c47667a0e367f4e1b464cc2875e023e950f1f049f1fd33` |
| Approved XML member | `a3163e14-0404-4e27-884b-f6f9f7f695bc.xml`; 168,862 bytes; SHA-256 `696ebb05a528236ea6077c912785e94cf103aa4d29fa61bacab3282e65307fd4` |
| Root identity in XML | `id/@root=a3163e14-0404-4e27-884b-f6f9f7f695bc`; `setId/@root=24610d9f-0c5a-4f55-93b3-d456300bfd5d`; `versionNumber/@value=3`; `effectiveTime/@value=20260113` |
| Original Figure 1 member | `lantidra-01.jpg`; JPEG, 866 x 433 pixels; 65,914 bytes; SHA-256 `6ad0706e8428c4d1cc81af7c38dc74d3e570c18fb56ac4cc313f52729f9f718a` |

ZIP and XML hashes match the frozen source manifest. The image hash is a new
AI-computed asset locator within that exact ZIP, not a replacement source
version or human approval. Retrieval/hash verification was performed at
approximately **2026-10-29T19:51Z**; the original JPEG was subsequently opened
locally for AI visual inspection. No OCR, digitization, participant-level
transcription, or alternative source retrieval was performed.

**Precise caption:** "Figure 1: Periods of Insulin Use and Insulin Independence
following Initial Infusion, by Patient (Pooled Population)".

**Locator:** in the approved XML, namespace `h=urn:hl7-org:v3`,
`//h:section[@ID='S14']/h:text/h:paragraph[@ID='Fig1']` holds the caption
in Section **14 CLINICAL STUDIES**, after Table 4 and its duration paragraph.
The next paragraph contains `h:renderMultiMedia[@referencedObject='MM1']`.
Within the same section,
`h:component/h:observationMedia[@ID='MM1']/h:value/h:reference/@value`
resolves to **`lantidra-01.jpg`** (`mediaType=image/jpeg`).
The paragraph immediately after the rendering reference explains the graphic.

**Reviewer access:** obtain archive 940595 from the official link, verify its
ZIP and XML identities above, then open the exact `lantidra-01.jpg` member
locally alongside Section 14. This is the verified, version-specific original
figure route; no independently verified stand-alone historical image URL is
claimed. A text-only XML viewer may show a placeholder instead of rendering
the image. Do not treat that placeholder as the figure or substitute a live
set-ID image endpoint that has not been bound to v3.

## Evidence boundary and legibility assessment

Everything in this section is **AI-prepared and pending authorized human source
verification of the actual frozen figure**, including apparently legible
labels. It is not a new field decision.

| Evidence surface | What this inspection supports | What it does not support |
|---|---|---|
| XML caption and explanatory paragraph | The figure covers individual histories; black denotes insulin use and white independence. Time zero is first infusion; arrows denote second/third infusions. | No numeric observed onset value or onset distribution is printed in that explanatory paragraph. Text-only review cannot establish that onset is absent from the graphic. |
| Original JPEG: broad layout | Study 1 and Study 2 groups, horizontal histories, black/white segments, infusion arrows and a legend are visible. The horizontal axis reads months after first treatment, with labeled ticks from 0 to 170 in steps of 10. | This axis scale is not a series of exact participant onset dates or a common follow-up horizon. A visible graphic does not establish exact event times. |
| Original JPEG: transitions and small marks | Individual histories contain transitions that could be evaluated for the first insulin-independent segment. | The original is only 866 x 433 pixels. Closely spaced early transitions, thin white segments and small arrows cannot all be confidently resolved in this inspection. No claim is made that every transition or arrow is legible. |
| Original JPEG: row identity | Histories are grouped by study. | No individual subject identifiers are legible in this inspected asset. Any future row labels must be explicitly analyst-assigned positional labels, not claimed source IDs or cross-study participant linkage. |
| Quantitative onset | At most, the graphic is a candidate for bounded, approximate graphical timing after first infusion, if a human can resolve each relevant transition and its scale. | No exact numeric onset, minimum/maximum, mean/median, distribution, row-level interval or onset classification has been extracted here. No graphical estimate is represented as source-tabulated data. |

Visual evidence was available locally; it was **not unavailable** in this run.
The limitation is unverified quantitative interpretation and finite native
resolution, not a claimed access failure. Enlargement may aid viewing but
cannot add source precision. The packet does not infer a time-to-independence
statistic from total independence durations in Table 4, the approved any-time
25/30 observation, or Patient Information counseling that independence can take
weeks. None establishes observed onset timing.

## Proposed authorized human extraction workflow

1. Confirm lawful individual access, exact archive/member identity, caption,
   legend and axis against the actual image. Record the human reviewer, date,
   material inspected and scope only after review occurs. This packet supplies
   no completed human sign-off.
2. Verify row coverage against the pooled all-treated target and source study
   groups before extracting. If using positional study/row labels, record the
   ordering convention and do not infer personal identities. Keep all histories,
   including those with no visible independent interval; do not select only
   responders or equate an unreadable interval with no independence.
3. For each readable history, identify the first transition to independence
   relative to **first** infusion. Distinguish onset from accumulated duration,
   loss/recovery of independence, and later infusion markers. If first onset
   occurs after another infusion, retain the first-infusion clock and record
   that relationship only if actually legible; do not reset time zero.
4. Record whether timing is explicitly labeled or graphically estimated.
   For an estimate, retain lower/upper graphical bounds, units, tick calibration,
   boundary ambiguity and resolution limits. Do not silently round to exact
   days or report a pixel-derived point as an observed source value. Mark
   unreadable/ambiguous rows unresolved, never zero or absent. Do not infer
   censoring, withdrawal, death or complete follow-up from a bar endpoint.
5. Have the authorized human verify any proposed extraction against the actual
   source, including early near-zero segments and repeated-treatment histories.
   If rights, rendering, resolution or interpretation prevent inspection,
   explicitly record unavailable/unreadable visual evidence and leave extraction
   pending rather than reconstructing it from text.
6. Submit a separate field-level proposal with exact locators, extraction method
   and limitations. Any AI-generated candidate remains explicitly AI-prepared
   until authorized human source verification of the actual figure. Do not
   promote either `reported` or `unreported_in_reviewed_material` from this
   packet. No new extraction format or rule interpretation is adopted here.

This is an extraction plan, not execution of participant-level digitization,
paired real-source classification, outcome aggregation or robustness analysis.
It cannot establish fixed day-365/month-12 efficacy or its analysis denominator.

## Rights, retention and gates

The manifest's approved exact-version handling and
[NLM copyright policy](https://www.nlm.nih.gov/web_policies.html#copyright)
were consulted. NLM distinguishes government works from potentially protected
privately contributed content and does not guarantee an item's copyright
status. Public access and ZIP membership do not establish that a manufacturer
figure is public domain or covered by the repository's license.

This packet contains factual annotations and a short identifying caption only.
No archive, XML, figure, crop, screenshot, tracing or derivative reconstruction
is committed, attached to the PR or redistributed. Temporary local source
copies used for this inspection are removed after the check. Reviewers should
use the official frozen route themselves under applicable terms; if additional
copying/sharing is needed, establish its rights basis first. No blanket
redistribution permission is asserted.

`independence.onset` remains `not_yet_extracted`, `value=null`,
`review_complete=false`. The other two pending fields remain pending.
`source_content_review_complete=false`, `adjudication_complete=false`,
access-attempt exhaustion remains unclaimed, and
`independent_review_pending=true`. Existing human decisions and printed source
discrepancies remain intact. No S18/S19 excluded material or restricted S23
content was accessed. No human attestation, independent scientific approval,
G2-B acceptance, Issue #35 unblocking or G2-C authorization is supplied.
