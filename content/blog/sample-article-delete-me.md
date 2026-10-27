---
title: "Sample post: every block the blog template can render"
description: "A draft that shows the cost table, photo, callout, call to action and FAQ blocks so the owner can check the design in a preview before the first real article."
pubDate: 2026-10-26
heroPhoto: sample-walk-in-shower
tags: [sample, template]
hub: bathroom
intent: how-to
targetQuery: "sample post template check"
sources:
  - { title: "Seattle SDCI: Do You Need a Permit?", url: "https://www.seattle.gov/sdci/permits/do-you-need-a-permit", accessed: 2026-10-26 }
ownerFactsUsed: ["Contact", "Process"]
draft: true
noindex: true
---

This is a sample post. It exists so the owner can see how every block looks in the site's design on a Cloudflare preview. Because it is a draft with noindex set, it never reaches the blog index, the RSS feed or the sitemap. Delete this file before the first real article, or keep it as a draft.

## What a cost table looks like

A cost table holds ranges with their scope. The block carries no prices of its own; every number here is a placeholder that a real article would take from the facts file or from a cited public source. Seattle adds sales tax as a separate line at the rate of the project address, and the article says so next to the table.

:::costtable
title: Placeholder ranges for the template check
updated: October 2026
note: Placeholder numbers only. Real articles cite the facts file or a public source with the month checked.
rows:
  - { item: "Keep-the-footprint refresh", low: "$X", high: "$Y", note: "placeholder" }
  - { item: "Full remodel, same footprint", low: "$X", high: "$Y", note: "placeholder" }
  - { item: "Layout change", low: "$X", high: "$Y", note: "placeholder" }
:::

The table above uses the site's line color and the gradient accent. On a phone it scrolls sideways instead of squeezing the columns.

## What a photo block and a callout look like

A photo block takes an id from the photo library, a caption and an alt text. The image below is a copy of a portfolio photo that is already on the site.

{{photo id="b13" caption="Dark wood vanity with a quartz top and a lit mirror." alt="Dark wood vanity with a quartz top and a lit mirror" size="half"}}

:::callout owner
On one job we opened a wall and found the old supply line was galvanized steel. We stopped, sent photos and a written price for the fix, and nothing moved forward until the client said yes. That is the rule on every project.
:::

:::callout warning
Washington requires the contractor registration number in every ad. Ours is TRUESRL759QK, and you can verify it on the L&I site before you sign anything.
:::

{{cta}}

## What the FAQ and the ending look like

Every article ends with a short FAQ of real questions, then the reviewer box the layout prints, then related posts and the booking form. Permit rules in Seattle come from [SDCI](https://www.seattle.gov/sdci/permits/do-you-need-a-permit) (checked October 2026). The service page this post belongs to is [bathroom remodeling in Seattle](/bathroom-remodeling). Call +1 206-222-2328 if you want to talk first.

:::faq
- q: Is this a real article?
  a: No. It is a draft that exists to check the template. It is not indexed and not listed in the blog.
- q: Where do the numbers in real articles come from?
  a: From content/business-facts.md when they are about TrueSquare, or from an official page with the month we checked it when they are about permits, taxes or codes.
- q: Who approves a post before it goes live?
  a: Serhii reads the preview and merges the pull request. Nothing is published without that step.
:::
