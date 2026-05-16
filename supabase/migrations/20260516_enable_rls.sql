-- Enable Row-Level Security for FilmFinder tables.
--
-- The app's backend code should use SUPABASE_SERVICE_ROLE_KEY for REST calls.
-- Service-role requests bypass RLS, while public anon/authenticated clients get
-- no direct table access unless a policy is added later.

alter table if exists public.subscriptions enable row level security;
alter table if exists public.listing_embeddings enable row level security;

revoke all on table public.subscriptions from anon, authenticated;
revoke all on table public.listing_embeddings from anon, authenticated;

