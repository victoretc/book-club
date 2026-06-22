import test from '@playwright/test';
import { LocatorProps } from '../types/page-factory/component';
import { Component } from './component';

export class Select extends Component {
  get typeOf(): string {
    return 'select';
  }

  async openDropdown(locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`Opening dropdown for ${this.typeOf} with name "${this.componentName}"`, async () => {
      const locator = this.getLocator(locatorProps);
      await locator.click();
    });
  }

  async closeDropdown(locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`Closing dropdown for ${this.typeOf} with name "${this.componentName}"`, async () => {
      const locator = this.getLocator(locatorProps);
      await locator.click();
    });
  }

  async searchOption(searchText: string, locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`Searching for "${searchText}" in ${this.typeOf} with name "${this.componentName}"`, async () => {
      const locator = this.getLocator(locatorProps);
      await locator.fill(searchText);
    });
  }

  async selectOptionByText(optionText: string, locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`Selecting option "${optionText}" in ${this.typeOf} with name "${this.componentName}"`, async () => {
      const option = this.getLocator(locatorProps).filter({ hasText: optionText });
      await option.click();
    });
  }

  async selectOptionByCode(currencyCode: string, locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`Selecting currency with code "${currencyCode}" in ${this.typeOf} with name "${this.componentName}"`, async () => {
      await this.openDropdown(locatorProps);
      const option = this.getLocator(locatorProps).filter({ hasText: currencyCode });
      await option.click();
    });
  }

  async getSelectedOption(locatorProps: LocatorProps = {}): Promise<string> {
    return await test.step(`Getting selected option for ${this.typeOf} with name "${this.componentName}"`, async () => {
      const selectedOption = this.getLocator(locatorProps);
      return await selectedOption.textContent() ?? '';
    });
  }

  async shouldHaveSelectedOption(expectedText: string, locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`${this.typeOfUpper} "${this.componentName}" should have selected option "${expectedText}"`, async () => {
      const actualText = await this.getSelectedOption(locatorProps);
      await expect(actualText).toContain(expectedText);
    });
  }

  async shouldHaveOptionsCount(expectedCount: number, locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`${this.typeOfUpper} "${this.componentName}" should have ${expectedCount} options`, async () => {
      await this.openDropdown(locatorProps);
      const options = this.getLocator(locatorProps);
      await expect(options).toHaveCount(expectedCount);
    });
  }

  async shouldHaveNoResultsMessage(locatorProps: LocatorProps = {}): Promise<void> {
    await test.step(`${this.typeOfUpper} "${this.componentName}" should show "no results" message`, async () => {
      await this.openDropdown(locatorProps);
      const message = this.getLocator(locatorProps);
      await expect(message).toBeVisible();
    });
  }
}