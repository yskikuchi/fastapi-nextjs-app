import { test, expect } from '@jest/globals';
import { calculateTotalPrice } from '../../../../features/booking/utils/calculate';

test('currect total price', () => {
  const car = {
    id: '12345',
    name: '車両A',
    capacity: 7,
    carNumber: 'あ 99-99',
    priceForInitialTwelveHours: 13000,
    pricePerAdditionalSixHours: 6000,
  };
  const startTime = new Date(2024, 10, 1, 12);
  const endTime = new Date(2024, 10, 3, 15);
  const result = calculateTotalPrice(car, startTime, endTime);
  expect(result).toBe(55000);
});
