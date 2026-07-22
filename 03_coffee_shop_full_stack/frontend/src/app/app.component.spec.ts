import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { TestBed, waitForAsync } from '@angular/core/testing';

import { Platform } from '@ionic/angular';

import { AppComponent } from './app.component';

const { setStyleMock, hideMock } = vi.hoisted(() => ({
    setStyleMock: vi.fn().mockResolvedValue(undefined),
    hideMock: vi.fn().mockResolvedValue(undefined),
}));

vi.mock('@capacitor/status-bar', () => ({
    StatusBar: { setStyle: setStyleMock },
    Style: { Default: 'DEFAULT' },
}));
vi.mock('@capacitor/splash-screen', () => ({
    SplashScreen: { hide: hideMock },
}));

describe('AppComponent', () => {

    let platformReadySpy: Promise<void>, platformSpy: { ready: ReturnType<typeof vi.fn> };

    beforeEach(waitForAsync(() => {
        setStyleMock.mockClear();
        hideMock.mockClear();
        platformReadySpy = Promise.resolve();
        platformSpy = {
            ready: vi.fn().mockName("Platform.ready").mockReturnValue(platformReadySpy)
        };

        TestBed.configureTestingModule({
            declarations: [AppComponent],
            schemas: [CUSTOM_ELEMENTS_SCHEMA],
            providers: [
                { provide: Platform, useValue: platformSpy },
            ],
        }).compileComponents();
    }));

    it('should create the app', () => {
        const fixture = TestBed.createComponent(AppComponent);
        const app = fixture.debugElement.componentInstance;
        expect(app).toBeTruthy();
    });

    it('should initialize the app', async () => {
        TestBed.createComponent(AppComponent);
        expect(platformSpy.ready).toHaveBeenCalled();
        await platformReadySpy;
        expect(setStyleMock).toHaveBeenCalled();
        expect(hideMock).toHaveBeenCalled();
    });

    // TODO: add more tests!

});
