import {
    extractShareLinksFromText,
    snippetFromShareMessages,
} from "./shareLink";

describe("share link utilities", () => {
    test("extracts decoded unique links while preserving query variants", () => {
        const text = [
            "https://misa.example/share/chat%2042?lang=ru",
            "/share/chat%2042?lang=ru",
            "/share/chat%2042?lang=en#preview",
        ].join(" ");

        expect(extractShareLinksFromText(text)).toEqual([
            { chatId: "chat 42", query: "lang=ru" },
            { chatId: "chat 42", query: "lang=en" },
        ]);
    });

    test("builds a bounded plain-text preview from the first useful message", () => {
        const longText = "word ".repeat(40).trim();

        const snippet = snippetFromShareMessages([
            { content: "```js\nconst hidden = true;\n```" },
            { content: `  ${longText}  ` },
        ]);

        expect(snippet).toHaveLength(160);
        expect(snippet.endsWith("…")).toBe(true);
        expect(snippet).not.toContain("hidden");
    });
});
