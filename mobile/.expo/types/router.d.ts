/* eslint-disable */
import * as Router from 'expo-router';

export * from 'expo-router';

declare module 'expo-router' {
  export namespace ExpoRouter {
    export interface __routes<T extends string | object = string> {
      hrefInputParams: { pathname: Router.RelativePathString, params?: Router.UnknownInputParams } | { pathname: Router.ExternalPathString, params?: Router.UnknownInputParams } | { pathname: `/login`; params?: Router.UnknownInputParams; } | { pathname: `/_sitemap`; params?: Router.UnknownInputParams; } | { pathname: `${'/(protected)'}` | `/`; params?: Router.UnknownInputParams; } | { pathname: `${'/(protected)'}/motorista` | `/motorista`; params?: Router.UnknownInputParams; } | { pathname: `/utils/authContext`; params?: Router.UnknownInputParams; };
      hrefOutputParams: { pathname: Router.RelativePathString, params?: Router.UnknownOutputParams } | { pathname: Router.ExternalPathString, params?: Router.UnknownOutputParams } | { pathname: `/login`; params?: Router.UnknownOutputParams; } | { pathname: `/_sitemap`; params?: Router.UnknownOutputParams; } | { pathname: `${'/(protected)'}` | `/`; params?: Router.UnknownOutputParams; } | { pathname: `${'/(protected)'}/motorista` | `/motorista`; params?: Router.UnknownOutputParams; } | { pathname: `/utils/authContext`; params?: Router.UnknownOutputParams; };
      href: Router.RelativePathString | Router.ExternalPathString | `/login${`?${string}` | `#${string}` | ''}` | `/_sitemap${`?${string}` | `#${string}` | ''}` | `${'/(protected)'}${`?${string}` | `#${string}` | ''}` | `/${`?${string}` | `#${string}` | ''}` | `${'/(protected)'}/motorista${`?${string}` | `#${string}` | ''}` | `/motorista${`?${string}` | `#${string}` | ''}` | `/utils/authContext${`?${string}` | `#${string}` | ''}` | { pathname: Router.RelativePathString, params?: Router.UnknownInputParams } | { pathname: Router.ExternalPathString, params?: Router.UnknownInputParams } | { pathname: `/login`; params?: Router.UnknownInputParams; } | { pathname: `/_sitemap`; params?: Router.UnknownInputParams; } | { pathname: `${'/(protected)'}` | `/`; params?: Router.UnknownInputParams; } | { pathname: `${'/(protected)'}/motorista` | `/motorista`; params?: Router.UnknownInputParams; } | { pathname: `/utils/authContext`; params?: Router.UnknownInputParams; };
    }
  }
}
