import { z } from "zod/v4";

export const TokenPairSchema = z.object({
  access_token: z.string(),
  refresh_token: z.string(),
  token_type: z.string(),
});

export const UserSchema = z.object({
  id: z.string(),
  email: z.email(),
  created_at: z.string(),
});

export const UrlSchema = z.object({
  id: z.string(),
  short_code: z.string(),
  original_url: z.string(),
  is_active: z.boolean(),
  created_at: z.string(),
});

export const UrlListSchema = z.array(UrlSchema);

export const ReferrerStatSchema = z.object({
  referrer: z.string(),
  count: z.number(),
});

export const CountryStatSchema = z.object({
  country: z.string(),
  count: z.number(),
});

export const ClickSchema = z.object({
  ip_address: z.string(),
  user_agent: z.string(),
  referrer: z.string(),
  country: z.string(),
  clicked_at: z.string().nullable(),
});

export const StatsSchema = z.object({
  short_code: z.string(),
  total_clicks: z.number(),
  top_referrers: z.array(ReferrerStatSchema),
  top_countries: z.array(CountryStatSchema),
  recent_clicks: z.array(ClickSchema),
});

export const ShortenResultSchema = z.object({
  short_code: z.string(),
  original_url: z.string(),
});

export type TokenPair = z.infer<typeof TokenPairSchema>;
export type User = z.infer<typeof UserSchema>;
export type Url = z.infer<typeof UrlSchema>;
export type Stats = z.infer<typeof StatsSchema>;
export type ShortenResult = z.infer<typeof ShortenResultSchema>;
