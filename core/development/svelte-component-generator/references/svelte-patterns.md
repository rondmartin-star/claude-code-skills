# Svelte 5 Patterns Reference

**Purpose:** Comprehensive guide to Svelte 5 patterns for component generation
**Version:** 1.0.0
**Date:** 2026-02-14

---

## Table of Contents

1. [Svelte 5 Runes](#svelte-5-runes)
2. [Component Structure](#component-structure)
3. [TypeScript Integration](#typescript-integration)
4. [State Management](#state-management)
5. [Event Handling](#event-handling)
6. [SSR vs CSR](#ssr-vs-csr)
7. [SvelteKit Integration](#sveltekit-integration)

---

## Svelte 5 Runes

### $state() - Reactive State

```svelte
<script lang="ts">
  // Simple state
  let count = $state(0);

  // Object state
  let user = $state({
    name: 'John',
    age: 30
  });

  // Array state
  let items = $state<string[]>([]);

  // Updating state
  function increment() {
    count++; // Direct mutation works!
  }

  function updateUser() {
    user.age++; // Direct object mutation
  }

  function addItem(item: string) {
    items.push(item); // Direct array mutation
  }
</script>
```

### $props() - Component Props

```svelte
<script lang="ts">
  // Destructured props with defaults
  let {
    variant = 'primary',
    size = 'md',
    disabled = false,
    children
  } = $props<{
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    children: Snippet;
  }>();

  // Alternative: Interface-based props
  export interface ButtonProps {
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
  }

  let {
    variant = 'primary',
    size = 'md',
    disabled = false
  }: ButtonProps = $props();
</script>
```

### $derived() - Computed Values

```svelte
<script lang="ts">
  let count = $state(0);

  // Simple derived
  let doubled = $derived(count * 2);

  // Complex derived with logic
  let status = $derived(
    count === 0 ? 'empty' :
    count < 10 ? 'low' :
    count < 100 ? 'medium' : 'high'
  );

  // Derived from props
  let {
    variant = 'primary',
    size = 'md',
    disabled = false
  } = $props();

  let classes = $derived(`
    btn
    btn-${variant}
    btn-${size}
    ${disabled ? 'btn-disabled' : ''}
  `.trim().replace(/\s+/g, ' '));
</script>
```

### $effect() - Side Effects

```svelte
<script lang="ts">
  let count = $state(0);

  // Run effect when count changes
  $effect(() => {
    console.log(`Count is now: ${count}`);

    // Cleanup function (optional)
    return () => {
      console.log('Cleanup previous effect');
    };
  });

  // Effect with dependencies
  let name = $state('');
  let age = $state(0);

  $effect(() => {
    // Only runs when name or age changes
    console.log(`${name} is ${age} years old`);
  });
</script>
```

---

## Component Structure

### Complete Component Template

```svelte
<script lang="ts">
  /**
   * Button - A customizable button component
   *
   * @component
   * @example
   * <Button variant="primary" size="md" on:click={handleClick}>
   *   Click me
   * </Button>
   */

  // 1. Imports
  import type { Snippet } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  // 2. Type Definitions
  export interface ButtonProps {
    variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    loading?: boolean;
    fullWidth?: boolean;
    type?: 'button' | 'submit' | 'reset';
    children?: Snippet;
  }

  // 3. Props with Defaults
  let {
    variant = 'primary',
    size = 'md',
    disabled = false,
    loading = false,
    fullWidth = false,
    type = 'button',
    children
  }: ButtonProps = $props();

  // 4. Local State
  let isHovered = $state(false);
  let isFocused = $state(false);

  // 5. Computed Values
  let classes = $derived(`
    inline-flex items-center justify-center font-medium rounded-md
    transition-colors duration-200 focus-visible:outline-none
    focus-visible:ring-2 focus-visible:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
    ${variantClasses[variant]}
    ${sizeClasses[size]}
    ${fullWidth ? 'w-full' : ''}
    ${isHovered && !disabled ? 'transform scale-105' : ''}
  `.trim().replace(/\s+/g, ' '));

  // 6. Style Maps
  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 focus-visible:ring-secondary-500',
    danger: 'bg-danger-600 text-white hover:bg-danger-700 focus-visible:ring-danger-500',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus-visible:ring-gray-500'
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  // 7. Event Handlers
  const dispatch = createEventDispatcher<{
    click: MouseEvent;
  }>();

  function handleClick(event: MouseEvent) {
    if (disabled || loading) {
      event.preventDefault();
      return;
    }
    dispatch('click', event);
  }
</script>

<!-- 8. Template -->
<button
  {type}
  class={classes}
  disabled={disabled || loading}
  aria-disabled={disabled || loading}
  aria-busy={loading}
  on:click={handleClick}
  on:mouseenter={() => isHovered = true}
  on:mouseleave={() => isHovered = false}
  on:focus={() => isFocused = true}
  on:blur={() => isFocused = false}
>
  {#if loading}
    <svg class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  {/if}

  {#if children}
    {@render children()}
  {:else}
    <slot />
  {/if}
</button>

<!-- 9. Scoped Styles (minimal - prefer Tailwind) -->
<style>
  /* Only include truly component-specific styles */
  button {
    /* Any non-Tailwind styles needed */
  }
</style>
```

---

## TypeScript Integration

### Type-Safe Props

```typescript
// Define props interface
export interface CardProps {
  title: string;
  description?: string;
  image?: {
    src: string;
    alt: string;
  };
  actions?: Array<{
    label: string;
    onClick: () => void;
  }>;
  variant?: 'elevated' | 'outlined' | 'filled';
}

// Use in component
let {
  title,
  description,
  image,
  actions = [],
  variant = 'elevated'
}: CardProps = $props();
```

### Type-Safe Events

```typescript
import { createEventDispatcher } from 'svelte';

// Define event types
type FormEvents = {
  submit: { values: Record<string, any> };
  cancel: never;
  change: { field: string; value: any };
};

const dispatch = createEventDispatcher<FormEvents>();

// Dispatch with type safety
dispatch('submit', { values: formData });
dispatch('cancel');
dispatch('change', { field: 'email', value: 'user@example.com' });
```

### Type-Safe Slots/Snippets

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    header,
    footer,
    children
  } = $props<{
    header?: Snippet;
    footer?: Snippet<[{ count: number }]>; // Snippet with parameters
    children?: Snippet;
  }>();

  let count = $state(0);
</script>

<div>
  {#if header}
    {@render header()}
  {/if}

  <main>
    {#if children}
      {@render children()}
    {:else}
      <slot />
    {/if}
  </main>

  {#if footer}
    {@render footer({ count })}
  {/if}
</div>
```

---

## State Management

### Component-Level State

```svelte
<script lang="ts">
  // Simple state
  let count = $state(0);

  // Object state
  let form = $state({
    email: '',
    password: '',
    rememberMe: false
  });

  // Array state
  let todos = $state<Array<{ id: number; text: string; done: boolean }>>([]);

  // Nested state
  let app = $state({
    user: {
      profile: { name: '', avatar: '' },
      settings: { theme: 'light' }
    },
    items: []
  });
</script>
```

### Shared State (Context)

```svelte
<!-- stores/theme.svelte.ts -->
<script lang="ts" context="module">
  export type Theme = 'light' | 'dark';

  class ThemeStore {
    current = $state<Theme>('light');

    toggle() {
      this.current = this.current === 'light' ? 'dark' : 'light';
    }

    set(theme: Theme) {
      this.current = theme;
    }
  }

  export const themeStore = new ThemeStore();
</script>

<!-- App.svelte -->
<script lang="ts">
  import { themeStore } from './stores/theme.svelte';

  // Use directly
  $effect(() => {
    document.documentElement.setAttribute('data-theme', themeStore.current);
  });
</script>

<div data-theme={themeStore.current}>
  <button on:click={() => themeStore.toggle()}>
    Toggle Theme (current: {themeStore.current})
  </button>
</div>
```

### URL State (SvelteKit)

```svelte
<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  // Read URL params
  $: searchTerm = $page.url.searchParams.get('q') || '';
  $: page = parseInt($page.url.searchParams.get('page') || '1');

  // Update URL
  function updateSearch(term: string) {
    const url = new URL($page.url);
    url.searchParams.set('q', term);
    goto(url.toString(), { replaceState: true });
  }
</script>
```

---

## Event Handling

### Native DOM Events

```svelte
<script lang="ts">
  function handleClick(event: MouseEvent) {
    console.log('Clicked at:', event.clientX, event.clientY);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      console.log('Enter pressed');
    }
  }

  function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget as HTMLFormElement);
    console.log(Object.fromEntries(formData));
  }
</script>

<button on:click={handleClick}>Click</button>
<input on:keydown={handleKeydown} />
<form on:submit={handleSubmit}>
  <input name="email" />
  <button type="submit">Submit</button>
</form>
```

### Custom Component Events

```svelte
<!-- Child.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  type Events = {
    select: { id: number; name: string };
    delete: { id: number };
  };

  const dispatch = createEventDispatcher<Events>();

  let { id, name } = $props<{ id: number; name: string }>();
</script>

<div>
  <button on:click={() => dispatch('select', { id, name })}>
    Select
  </button>
  <button on:click={() => dispatch('delete', { id })}>
    Delete
  </button>
</div>

<!-- Parent.svelte -->
<script lang="ts">
  import Child from './Child.svelte';

  function handleSelect(event: CustomEvent<{ id: number; name: string }>) {
    console.log('Selected:', event.detail);
  }

  function handleDelete(event: CustomEvent<{ id: number }>) {
    console.log('Deleted:', event.detail.id);
  }
</script>

<Child
  id={1}
  name="Item 1"
  on:select={handleSelect}
  on:delete={handleDelete}
/>
```

### Event Forwarding

```svelte
<!-- Wrapper.svelte -->
<script lang="ts">
  import Button from './Button.svelte';
</script>

<!-- Forward click event to parent -->
<Button on:click>Click me</Button>

<!-- Parent.svelte -->
<script lang="ts">
  import Wrapper from './Wrapper.svelte';

  function handleClick() {
    console.log('Button clicked through wrapper!');
  }
</script>

<Wrapper on:click={handleClick} />
```

---

## SSR vs CSR

### Server-Side Rendering (SSR)

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  // This runs on server during SSR
  export let data: PageData;

  // Access server-loaded data
  $: ({ posts, user } = data);
</script>

<div>
  <h1>Welcome, {user.name}</h1>
  <ul>
    {#each posts as post}
      <li>{post.title}</li>
    {/each}
  </ul>
</div>

<!-- +page.server.ts -->
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
  // Runs ONLY on server
  const posts = await fetch('/api/posts').then(r => r.json());
  const user = await getUser(params.userId);

  return {
    posts,
    user
  };
};
```

### Client-Side Only Code

```svelte
<script lang="ts">
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';

  let width = $state(0);

  // Run only in browser
  if (browser) {
    width = window.innerWidth;
  }

  // Or use onMount (always runs client-side)
  onMount(() => {
    width = window.innerWidth;

    const handleResize = () => {
      width = window.innerWidth;
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });
</script>

<div>Window width: {width}px</div>
```

### Hybrid (Universal) Code

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  import { page } from '$app/stores';

  // Server provides initial data
  export let data: PageData;

  // Client can update data
  let items = $state(data.items);

  async function loadMore() {
    const response = await fetch(`/api/items?page=${items.length / 10 + 1}`);
    const newItems = await response.json();
    items = [...items, ...newItems];
  }
</script>

<ul>
  {#each items as item}
    <li>{item.title}</li>
  {/each}
</ul>

<button on:click={loadMore}>Load More</button>
```

---

## SvelteKit Integration

### Page Components

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;

  $: ({ post, relatedPosts } = data);
</script>

<article>
  <h1>{post.title}</h1>
  <div>{@html post.content}</div>

  <aside>
    <h2>Related Posts</h2>
    {#each relatedPosts as related}
      <a href="/blog/{related.slug}">{related.title}</a>
    {/each}
  </aside>
</article>
```

### Layout Components

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from './$types';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';

  export let data: LayoutData;

  $: ({ user } = data);
</script>

<div class="app">
  <Navbar {user} />

  <main>
    <slot />
  </main>

  <Footer />
</div>
```

### API Routes

```typescript
// src/routes/api/posts/+server.ts
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ url }) => {
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = parseInt(url.searchParams.get('limit') || '10');

  const posts = await db.posts.findMany({
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' }
  });

  return json(posts);
};

export const POST: RequestHandler = async ({ request }) => {
  const data = await request.json();

  const post = await db.posts.create({
    data: {
      title: data.title,
      content: data.content,
      authorId: data.authorId
    }
  });

  return json(post, { status: 201 });
};
```

### Form Actions

```svelte
<!-- src/routes/login/+page.svelte -->
<script lang="ts">
  import type { ActionData } from './$types';

  export let form: ActionData;
</script>

<form method="POST">
  {#if form?.error}
    <p class="error">{form.error}</p>
  {/if}

  <input name="email" type="email" required />
  <input name="password" type="password" required />
  <button type="submit">Login</button>
</form>

<!-- src/routes/login/+page.server.ts -->
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email');
    const password = data.get('password');

    const user = await authenticateUser(email, password);

    if (!user) {
      return fail(400, { error: 'Invalid credentials' });
    }

    cookies.set('session', user.sessionToken, {
      path: '/',
      httpOnly: true,
      sameSite: 'strict',
      secure: process.env.NODE_ENV === 'production',
      maxAge: 60 * 60 * 24 * 7 // 1 week
    });

    throw redirect(303, '/dashboard');
  }
};
```

---

## Best Practices

1. **Use Svelte 5 Runes:** Prefer $state, $props, $derived over legacy reactive declarations
2. **TypeScript Everything:** Type all props, events, and state for better DX
3. **Accessibility First:** Include ARIA attributes and keyboard navigation
4. **Tailwind over CSS:** Use utility classes, minimize custom styles
5. **Component Composition:** Break complex components into smaller pieces
6. **SSR-Friendly:** Avoid browser-only APIs at top level
7. **Form Actions:** Use SvelteKit form actions for better UX
8. **Error Boundaries:** Handle errors gracefully with error pages

---

*Last Updated: 2026-02-14*
*Version: 1.0.0*
