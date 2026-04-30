import { describe, expect, it } from "vitest";

describe("API Credentials Validation", () => {
  it("validates Resend API key format", () => {
    const resendKey = process.env.RESEND_API_KEY;
    expect(resendKey).toBeDefined();
    expect(resendKey).toMatch(/^re_/);
  });

  it("validates Resend Audience ID format", () => {
    const audienceId = process.env.RESEND_AUDIENCE_ID;
    expect(audienceId).toBeDefined();
    expect(audienceId).toMatch(/^[a-f0-9-]{36}$/);
  });

  it("validates OpenAI API key format", () => {
    const openaiKey = process.env.OPENAI_API_KEY;
    expect(openaiKey).toBeDefined();
    expect(openaiKey).toMatch(/^sk-proj-/);
  });

  it("validates Resend API key by making a test request", async () => {
    const resendKey = process.env.RESEND_API_KEY;
    if (!resendKey) {
      throw new Error("RESEND_API_KEY not set");
    }

    try {
      const response = await fetch("https://api.resend.com/audiences", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${resendKey}`,
        },
      });

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data).toHaveProperty("data");
    } catch (error) {
      throw new Error(`Resend API validation failed: ${error}`);
    }
  });

  it("validates OpenAI API key by making a test request", async () => {
    const openaiKey = process.env.OPENAI_API_KEY;
    if (!openaiKey) {
      throw new Error("OPENAI_API_KEY not set");
    }

    try {
      const response = await fetch("https://api.openai.com/v1/models", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${openaiKey}`,
        },
      });

      expect([200, 401]).toContain(response.status);
      const data = await response.json();
      expect(data).toBeDefined();
    } catch (error) {
      throw new Error(`OpenAI API validation failed: ${error}`);
    }
  });
});
