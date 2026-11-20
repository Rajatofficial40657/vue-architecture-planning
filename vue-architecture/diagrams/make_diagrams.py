import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages

C = {
    "view": ("#E6F1FB", "#185FA5"),
    "comp": ("#E1F5EE", "#0F6E56"),
    "store": ("#FAEEDA", "#854F0B"),
    "svc": ("#EEEDFE", "#534AB7"),
    "ext": ("#F1EFE8", "#5F5E5A"),
    "router": ("#FBEAF0", "#993556"),
    "comp2": ("#EAF3DE", "#3B6D11"),
}


def box(ax, x, y, w, h, text, kind="comp", fs=9, bold=False):
    fc, ec = C[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color="#222", fontweight="bold" if bold else "normal", linespacing=1.3)


def arrow(ax, p1, p2, label=None, color="#444", style="-|>", rad=0.0, ls="-", lpos=0.5, dx=0, dy=0):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=13, lw=1.3, color=color,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls)
    ax.add_patch(a)
    if label:
        mx = p1[0] + (p2[0] - p1[0]) * lpos + dx
        my = p1[1] + (p2[1] - p1[1]) * lpos + dy
        ax.text(mx, my, label, fontsize=7.5, ha="center", va="center", color=color,
                bbox=dict(fc="white", ec="none", pad=1.2))


def canvas(w, h, title, sub=None):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.text(w / 2, h - 0.35, title, ha="center", fontsize=15, fontweight="bold")
    if sub:
        ax.text(w / 2, h - 0.75, sub, ha="center", fontsize=9, color="#555")
    return fig, ax


# ---------------------------------------------------------------- Diagram 1
def diagram_architecture():
    W, H = 16, 11
    fig, ax = canvas(W, H, "Diagram 1 – Layered Architecture & Unidirectional Data Flow",
                     "Vue 3 + Vite + TypeScript · Pinia · Vue Router 4 · Axios")

    # Layer bands
    bands = [
        (8.2, 1.75, "PRESENTATION LAYER", "#F5F9FD"),
        (5.9, 1.9, "STATE LAYER (Pinia)", "#FEF8EE"),
        (3.7, 1.8, "DOMAIN / API LAYER", "#F7F6FE"),
        (1.0, 2.3, "EXTERNAL", "#F7F6F2"),
    ]
    for y, h, lbl, col in bands:
        ax.add_patch(FancyBboxPatch((0.3, y), W - 0.6, h, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    fc=col, ec="#CCC", lw=0.8))
        ax.text(0.5, y + h - 0.22, lbl, fontsize=9, fontweight="bold", color="#777")

    # Presentation
    box(ax, 0.8, 8.35, 2.6, 0.9, "Vue Router 4\n(guards, lazy routes)", "router")
    box(ax, 4.0, 8.35, 2.6, 0.9, "DashboardView\n(page / container)", "view", bold=True)
    box(ax, 7.2, 8.35, 2.6, 0.9, "Feature components\nStatsCard · ActivityFeed\nProfileCard · ChartPanel", "comp", fs=8)
    box(ax, 10.4, 8.35, 2.4, 0.9, "Composables\nuseDashboard()\nuseAuth()", "comp2", fs=8.5)
    box(ax, 13.2, 8.35, 2.2, 0.9, "Shared UI\nBaseButton · BaseCard\nBaseModal", "comp", fs=8)

    # State
    box(ax, 1.2, 6.2, 3.1, 1.1, "auth store\nuser · token · isLoggedIn\nlogin() logout() refresh()", "store", fs=8.5)
    box(ax, 5.0, 6.2, 3.3, 1.1, "dashboard store\nstats · activities · loading · error\nfetchAll() markRead()", "store", fs=8.5)
    box(ax, 9.0, 6.2, 3.0, 1.1, "settings store\ntheme · locale · layout\npersisted (localStorage)", "store", fs=8.5)
    box(ax, 12.6, 6.2, 2.7, 1.1, "Pinia plugins\nPersistence · Logger", "store", fs=8.5)

    # Domain/API
    box(ax, 1.2, 4.0, 2.9, 1.1, "authService.ts\nlogin · refresh · me", "svc", fs=9)
    box(ax, 4.7, 4.0, 3.1, 1.1, "dashboardService.ts\ngetStats · getActivities", "svc", fs=9)
    box(ax, 8.4, 4.0, 3.0, 1.1, "http client (Axios)\ninterceptors: token,\n401 refresh, error map", "svc", fs=8.5)
    box(ax, 13.0, 4.0, 2.4, 1.1, "types/ + DTO\nmappers", "svc", fs=8.5)

    # External
    box(ax, 3.0, 1.4, 3.6, 1.2, "REST / GraphQL Backend\n/auth  /stats  /activities", "ext", bold=True)
    box(ax, 10.9, 1.4, 3.0, 1.2, "Browser Storage\nlocalStorage / cookies", "ext")

    # Flow arrows
    arrow(ax, (3.4, 8.8), (4.0, 8.8), "navigates", "#993556")
    arrow(ax, (6.6, 8.8), (7.2, 8.8), "renders", "#0F6E56")
    arrow(ax, (9.8, 8.8), (10.4, 8.8), "uses", "#3B6D11")
    arrow(ax, (11.6, 8.35), (7.5, 7.3), "read state / call actions", "#854F0B", rad=-0.15, lpos=0.5)
    arrow(ax, (5.2, 8.35), (6.0, 7.3), "", "#185FA5")
    arrow(ax, (6.0, 6.2), (6.0, 5.1), "actions call services", "#534AB7", dx=1.0)
    arrow(ax, (2.7, 6.2), (2.7, 5.1), "", "#534AB7")
    arrow(ax, (7.8, 4.55), (8.4, 4.55), "", "#534AB7")
    arrow(ax, (4.1, 4.55), (4.7, 4.55), "", "#534AB7", style="<|-|>")
    arrow(ax, (9.0, 4.0), (6.3, 2.6), "HTTP (JSON)", "#5F5E5A", rad=0.0)
    arrow(ax, (11.5, 6.2), (12.4, 2.6), "persist", "#5F5E5A", ls="--", lpos=0.2, dx=0.5)
    # return path
    arrow(ax, (4.2, 2.6), (3.0, 4.0), "response", "#5F5E5A", rad=0.0, dx=-0.5)
    arrow(ax, (7.0, 5.1), (7.0, 6.2), "", "#534AB7", ls=":")

    # Legend / rules
    ax.text(0.5, 0.65, "Rules:  ① Components never call Axios directly   ② Only stores mutate shared state   "
                       "③ Services are pure, framework-agnostic   ④ Data flows down (props), events flow up (emits)",
            fontsize=9, color="#333")
    fig.savefig("diagrams/01_layered_architecture.png", dpi=170, bbox_inches="tight")
    return fig


# ---------------------------------------------------------------- Diagram 2
def diagram_components():
    W, H = 16, 11.2
    fig, ax = canvas(W, H, "Diagram 2 – Dashboard Component Hierarchy & Data Flow",
                     "Container/presentational split · props down · events up · Pinia for shared state")

    box(ax, 6.0, 9.4, 4.0, 0.8, "App.vue", "ext", bold=True, fs=11)
    box(ax, 6.0, 8.0, 4.0, 0.9, "DashboardLayout.vue\n(<router-view/>, sidebar slot)", "view", fs=9)
    box(ax, 5.5, 6.5, 5.0, 1.0, "DashboardView.vue  [CONTAINER]\nuses useDashboard() · owns no business logic", "view", bold=True, fs=9)
    box(ax, 12.3, 8.0, 3.3, 0.9, "Vue Router\n/dashboard → lazy view", "router", fs=9)
    arrow(ax, (8.0, 9.4), (8.0, 8.9), "", "#444")
    arrow(ax, (8.0, 8.0), (8.0, 7.5), "", "#444")
    arrow(ax, (12.3, 8.45), (10.0, 8.45), "mounts", "#993556")

    # stores + service (left column)
    box(ax, 0.4, 8.0, 3.4, 1.0, "Pinia: authStore\nuser · permissions", "store", fs=9)
    box(ax, 0.4, 6.4, 3.4, 1.2, "Pinia: dashboardStore\nstats · activities\nloading · error", "store", fs=9)
    box(ax, 0.4, 4.95, 2.5, 0.85, "dashboardService\n(Axios → REST API)", "svc", fs=9)
    arrow(ax, (3.8, 8.3), (5.5, 7.35), "read user", "#854F0B", dx=-0.1, dy=0.2)
    arrow(ax, (5.5, 6.95), (3.8, 6.95), "", "#854F0B")
    arrow(ax, (3.8, 7.25), (5.5, 7.25), "", "#854F0B")
    ax.text(4.65, 7.55, "state ⟵ ⟶ actions", fontsize=7.5, color="#854F0B", ha="center")
    arrow(ax, (1.6, 6.4), (1.6, 5.8), "fetchAll()", "#534AB7", ls="--", dx=0.85)

    # children
    kids = [
        (0.4, "AppSidebar\n(nav links from\nroute meta)"),
        (3.5, "DashboardHeader\n(search, user menu,\ntheme toggle)"),
        (6.6, "StatsGrid\n(layout only)"),
        (9.7, "ActivityFeed\n(list + filters)"),
        (12.8, "ProfileCard\n(user summary)"),
    ]
    for x, t in kids:
        box(ax, x, 3.5, 2.8, 1.2, t, "comp", fs=8.5)
        arrow(ax, (8.0, 6.5), (x + 1.4, 4.7), "", "#0F6E56")
    ax.text(8.0, 5.55, "props ↓", fontsize=8, color="#0F6E56", ha="center",
            bbox=dict(fc="white", ec="none", pad=1.5))

    # leafs
    box(ax, 5.2, 1.7, 2.4, 1.0, "StatCard × N\nprops: label,\nvalue, trend", "comp2", fs=8.5)
    box(ax, 8.0, 1.7, 2.4, 1.0, "ChartPanel\nprops: series\n(lazy-loaded)", "comp2", fs=8.5)
    box(ax, 10.9, 1.7, 2.4, 1.0, "ActivityItem × N\nprops: item\nemit: read", "comp2", fs=8.5)
    box(ax, 13.5, 1.7, 2.1, 1.0, "BaseAvatar\nBaseButton", "comp2", fs=8.5)
    arrow(ax, (8.0, 3.5), (6.4, 2.7), "", "#3B6D11")
    arrow(ax, (8.0, 3.5), (9.2, 2.7), "", "#3B6D11")
    arrow(ax, (11.1, 3.5), (12.1, 2.7), "", "#3B6D11")
    arrow(ax, (14.2, 3.5), (14.5, 2.7), "", "#3B6D11")
    # event up
    arrow(ax, (11.6, 2.7), (11.0, 3.5), "", "#B03A2E", ls="--", rad=-0.3)
    ax.text(10.35, 3.15, "emit('read') ↑", fontsize=7.5, color="#B03A2E", ha="center")

    # legend
    items = [("view", "View / container"), ("comp", "Feature component"), ("comp2", "Presentational / shared"),
             ("store", "Pinia store"), ("svc", "Service")]
    x = 0.6
    for k, t in items:
        box(ax, x, 0.4, 0.35, 0.3, "", k)
        ax.text(x + 0.5, 0.55, t, fontsize=8.5, va="center")
        x += 2.9
    ax.text(0.6, 1.1, "Green = props down   ·   Red dashed = events up   ·   Brown = reactive state & action calls   ·   "
                      "Purple dashed = async API request", fontsize=8.5, color="#444")
    fig.savefig("diagrams/02_component_hierarchy.png", dpi=170, bbox_inches="tight")
    return fig


# ---------------------------------------------------------------- Diagram 3
def diagram_routing():
    W, H = 16, 10.2
    fig, ax = canvas(W, H, "Diagram 3 – Modular Routing Structure & Navigation Guard Flow",
                     "Each feature module exports its own routes · lazy-loaded chunks · global guards")

    box(ax, 6.2, 8.2, 3.6, 0.95, "router/index.ts · createRouter()\nmerges module routes + guards", "router", bold=True, fs=9)

    mods = [
        (0.6, "modules/auth\n/login  /register\nmeta: guestOnly"),
        (4.5, "modules/dashboard\n/dashboard\n/dashboard/analytics\nmeta: requiresAuth"),
        (8.4, "modules/profile\n/profile  /profile/settings\nmeta: requiresAuth"),
        (12.3, "modules/admin\n/admin/users\nmeta: roles=['admin']"),
    ]
    for x, t in mods:
        box(ax, x, 6.5, 3.1, 1.3, t, "view", fs=8.5)
        arrow(ax, (8.0, 8.2), (x + 1.55, 7.8), "", "#993556")

    for x, t in [(0.6, "chunk: auth.js"), (4.5, "chunk: dashboard.js"), (8.4, "chunk: profile.js"), (12.3, "chunk: admin.js")]:
        box(ax, x, 5.3, 3.1, 0.7, t, "ext", fs=8.5)
        arrow(ax, (x + 1.55, 6.5), (x + 1.55, 6.0), "", "#5F5E5A")
    ax.text(8.0, 6.22, "", fontsize=8)
    ax.text(15.9, 6.2, "lazy import()", fontsize=7.5, color="#5F5E5A", ha="right")

    # guard flow
    ax.text(0.5, 4.7, "Global navigation guard flow (router.beforeEach)", fontsize=11, fontweight="bold")
    box(ax, 0.5, 3.4, 2.2, 0.9, "Navigation\nrequested", "ext", fs=9)
    box(ax, 3.4, 3.4, 2.6, 0.9, "route.meta\nrequiresAuth?", "router", fs=9)
    box(ax, 6.8, 3.4, 2.6, 0.9, "authStore\nisLoggedIn?", "store", fs=9)
    box(ax, 10.2, 3.4, 2.6, 0.9, "meta.roles\nmatch user?", "store", fs=9)
    box(ax, 13.4, 3.4, 2.2, 0.9, "next()\nrender view", "comp", fs=9, bold=True)
    arrow(ax, (2.7, 3.85), (3.4, 3.85), "", "#444")
    arrow(ax, (6.0, 3.85), (6.8, 3.85), "yes", "#444")
    arrow(ax, (9.4, 3.85), (10.2, 3.85), "yes", "#444")
    arrow(ax, (12.8, 3.85), (13.4, 3.85), "yes", "#444")
    box(ax, 3.4, 1.6, 2.6, 0.9, "No → next()\n(public route)", "comp", fs=8.5)
    box(ax, 6.8, 1.6, 2.6, 0.9, "No → redirect\n/login?redirect=…", "ext", fs=8.5)
    box(ax, 10.2, 1.6, 2.6, 0.9, "No → redirect\n/403 or /dashboard", "ext", fs=8.5)
    arrow(ax, (4.7, 3.4), (4.7, 2.5), "no", "#444")
    arrow(ax, (8.1, 3.4), (8.1, 2.5), "no", "#444")
    arrow(ax, (11.5, 3.4), (11.5, 2.5), "no", "#444")

    ax.text(0.5, 0.7, "Route meta: { requiresAuth, guestOnly, roles, title, layout }  ·  "
                       "Per-route: beforeEnter (optional data prefetch)  ·  scrollBehavior & 404 catch-all in router/index.ts",
            fontsize=8.8, color="#333")
    fig.savefig("diagrams/03_routing_and_guards.png", dpi=170, bbox_inches="tight")
    return fig


figs = [diagram_architecture(), diagram_components(), diagram_routing()]
with PdfPages("diagrams/architecture_diagrams.pdf") as pdf:
    for f in figs:
        pdf.savefig(f, bbox_inches="tight")
print("done")
