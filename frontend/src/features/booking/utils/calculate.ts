import { Car } from '@/types/car';

export const calculateTotalPrice = (
  selectedCar: Car | undefined,
  startTime: Date,
  endTime: Date
) => {
  const priceForInitialTwelveHours = selectedCar?.priceForInitialTwelveHours;
  const pricePerAdditionalSixHours = selectedCar?.pricePerAdditionalSixHours;
  const diffInMSec = endTime.getTime() - startTime.getTime();
  const diffInHours = diffInMSec / 1000 / 60 / 60;

  if (!priceForInitialTwelveHours || !pricePerAdditionalSixHours) return 0;
  if (diffInMSec < 0) return 0;

  if (diffInHours <= 12) {
    return priceForInitialTwelveHours;
  } else {
    const additionalHours = diffInHours - 12;
    const totalPrice =
      priceForInitialTwelveHours +
      Math.ceil(additionalHours / 6) * pricePerAdditionalSixHours;
    return totalPrice;
  }
};
