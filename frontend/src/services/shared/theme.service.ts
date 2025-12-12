class ThemeService {
    private themeKey = 'selected-theme';
    private prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    constructor() {
        this.prefersDark.addEventListener('change', (event) => this.handleSystemChange(event));
    }

    initializeTheme() {
        const storedTheme = localStorage.getItem(this.themeKey) as 'light' | 'dark' | 'system' | null;

        if (storedTheme) {
            this.setTheme(storedTheme);
        } else {
            this.setTheme('light');
        }
    }

    setTheme(theme: 'light' | 'dark' | 'system') {
        if (theme === 'system') {
            this.applySystemTheme();
        } else {
            document.documentElement.setAttribute('prefers-color-scheme', theme);
            this.applyThemeClass(theme === 'dark');
        }

        localStorage.setItem(this.themeKey, theme);
    }

    getTheme(): 'light' | 'dark' | 'system' {
        return (localStorage.getItem(this.themeKey) as 'light' | 'dark' | 'system') || 'system';
    }

    private applySystemTheme() {
        const isDarkMode = this.prefersDark.matches;
        this.applyThemeClass(isDarkMode);
    }

    private handleSystemChange(event: MediaQueryListEvent) {
        const storedTheme = localStorage.getItem(this.themeKey);

        if (storedTheme === 'system') {
            this.applyThemeClass(event.matches);
        }
    }

    private applyThemeClass(isDark: boolean) {
        document.documentElement.classList.toggle('ion-palette-dark', isDark);
    }
}

export default new ThemeService();
