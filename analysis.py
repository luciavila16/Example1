import csv
from html import escape
from pathlib import Path


def write_step_plot(days: list[str], steps: list[int], output_path: Path) -> None:
    width = 900
    height = 520
    left = 90
    top = 70
    chart_width = 780
    chart_height = 320
    maximum = max(steps, default=0)
    scale_max = max(2000, ((maximum + 1999) // 2000) * 2000)
    slot_width = chart_width / max(len(steps), 1)
    bar_width = slot_width * 0.62

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="450" y="35" text-anchor="middle" font-family="Arial" font-size="22">Daily steps</text>',
    ]

    for tick in range(7):
        value = scale_max * tick / 6
        y = top + chart_height - chart_height * tick / 6
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + chart_width}" y2="{y:.1f}" stroke="#dddddd"/>'
        )
        elements.append(
            f'<text x="{left - 12}" y="{y + 5:.1f}" text-anchor="end" font-family="Arial" font-size="13">{value:,.0f}</text>'
        )

    for index, (day, value) in enumerate(zip(days, steps)):
        x = left + slot_width * index + (slot_width - bar_width) / 2
        bar_height = chart_height * value / scale_max
        y = top + chart_height - bar_height
        elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" fill="#4285f4"/>'
        )
        elements.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-family="Arial" font-size="13">{value:,}</text>'
        )
        elements.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{top + chart_height + 28}" text-anchor="middle" font-family="Arial" font-size="13">{escape(day)}</text>'
        )

    elements.extend(
        [
            f'<line x1="{left}" y1="{top + chart_height}" x2="{left + chart_width}" y2="{top + chart_height}" stroke="#333333"/>',
            f'<text x="22" y="{top + chart_height / 2}" text-anchor="middle" font-family="Arial" font-size="14" transform="rotate(-90 22 {top + chart_height / 2})">Steps</text>',
            "</svg>",
        ]
    )
    output_path.write_text("\n".join(elements), encoding="utf-8")


def main() -> None:
    csv_path = Path(__file__).with_name("passi.csv")
    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    days = [row["giorno"] for row in rows]
    steps = [int(row["passi"]) for row in rows]
    total_steps = sum(steps)
    plot_path = Path(__file__).with_name("passi_plot.svg")

    write_step_plot(days, steps, plot_path)
    print(f"Total steps: {total_steps}")
    print(f"Plot saved to: {plot_path}")


if __name__ == "__main__":
    main()
