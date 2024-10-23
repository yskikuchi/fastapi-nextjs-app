/**
 * @jest-environment jsdom
 */

import { test, expect } from '@jest/globals';
import { useBookingForm } from '../../../../features/booking/hooks/useBookingForm';
import { renderHook } from '@testing-library/react';

test('useBookingForm', () => {
  const { result } = renderHook(() => useBookingForm());
  expect(result.current.startTime).toEqual(
    new Date(new Date().setHours(0, 0, 0, 0))
  );
  // 何をテストすべきかわからない...(´・ω・｀)
});
