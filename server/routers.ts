import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router } from "./_core/trpc";
import { z } from "zod";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  newsletter: router({
    subscribe: publicProcedure
      .input(z.object({ email: z.string().email() }))
      .mutation(async ({ input }) => {
        const resendApiKey = process.env.RESEND_API_KEY;
        const audienceId = process.env.RESEND_AUDIENCE_ID;

        if (!resendApiKey || !audienceId) {
          throw new Error("Resend API configuration missing");
        }

        const response = await fetch(
          `https://api.resend.com/audiences/${audienceId}/contacts`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${resendApiKey}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: input.email,
            }),
          }
        );

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || "Failed to subscribe");
        }

        return { success: true };
      }),

    getSubscriberCount: publicProcedure.query(async () => {
      const resendApiKey = process.env.RESEND_API_KEY;
      const audienceId = process.env.RESEND_AUDIENCE_ID;

      if (!resendApiKey || !audienceId) {
        return { count: 0 };
      }

      try {
        const response = await fetch(
          `https://api.resend.com/audiences/${audienceId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${resendApiKey}`,
            },
          }
        );

        if (!response.ok) {
          return { count: 0 };
        }

        const data = await response.json();
        return { count: data.contacts_count || 0 };
      } catch (error) {
        return { count: 0 };
      }
    }),
  }),
});

export type AppRouter = typeof appRouter;
