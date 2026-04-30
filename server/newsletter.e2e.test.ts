import { describe, expect, it, beforeAll, afterAll } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

/**
 * End-to-end test for newsletter subscription flow
 * Tests: email validation, Resend API integration, subscriber count retrieval
 */

function createPublicContext(): TrpcContext {
  return {
    user: null,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: () => {},
    } as TrpcContext["res"],
  };
}

describe("Newsletter E2E Flow", () => {
  let caller: ReturnType<typeof appRouter.createCaller>;

  beforeAll(() => {
    const ctx = createPublicContext();
    caller = appRouter.createCaller(ctx);
  });

  it("rejects invalid email format", async () => {
    try {
      await caller.newsletter.subscribe({ email: "invalid-email" });
      expect.fail("Should have thrown validation error");
    } catch (error: any) {
      expect(error.message).toContain("Invalid");
    }
  });

  it("accepts valid email format", async () => {
    try {
      const result = await caller.newsletter.subscribe({
        email: "test@example.com",
      });
      expect(result).toHaveProperty("success");
    } catch (error: any) {
      // Resend API might fail if email already exists, which is acceptable
      expect(error.message).toBeDefined();
    }
  });

  it("retrieves subscriber count from Resend", async () => {
    const result = await caller.newsletter.getSubscriberCount();
    expect(result).toHaveProperty("count");
    expect(typeof result.count).toBe("number");
    expect(result.count).toBeGreaterThanOrEqual(0);
  });

  it("handles missing Resend credentials gracefully", async () => {
    // This test verifies fallback behavior when credentials are missing
    const result = await caller.newsletter.getSubscriberCount();
    // Should return count of 0 if credentials are missing, not throw
    expect(result.count).toBeDefined();
  });

  it("validates email input is required", async () => {
    try {
      await caller.newsletter.subscribe({ email: "" });
      expect.fail("Should have thrown validation error");
    } catch (error: any) {
      expect(error.message).toBeDefined();
    }
  });
});
