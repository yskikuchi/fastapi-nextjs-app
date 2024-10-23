import { ChangeEvent, useState } from 'react';
import { useFetchCars } from './useFetchCars';
import { calculateTotalPrice } from '../utils/calculate';

export const useBookingForm = () => {
  const [startTime, setStartTime] = useState<Date>(
    new Date(new Date().setHours(0, 0, 0, 0))
  );
  const [endTime, setEndTime] = useState<Date>(
    new Date(new Date().setHours(0, 0, 0, 0))
  );
  const [firstName, setFirstName] = useState<string>('');
  const [lastName, setLastName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [totalAmount, setTotalAmount] = useState<number>(0);

  const { cars, selectedCar, setSelectedCar } = useFetchCars();

  const handleLastNameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setLastName(e.target.value);
  };

  const handleFirstNameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFirstName(e.target.value);
  };

  const handleStartTimeChange = (date: Date) => {
    setStartTime(date);
    setTotalAmount(calculateTotalPrice(selectedCar, date, endTime));
  };

  const handleEndTimeChange = (date: Date) => {
    setEndTime(date);
    setTotalAmount(calculateTotalPrice(selectedCar, startTime, date));
  };

  return {
    startTime,
    endTime,
    firstName,
    lastName,
    email,
    setEmail,
    selectedCar,
    setSelectedCar,
    totalAmount,
    cars,
    handleLastNameChange,
    handleFirstNameChange,
    handleStartTimeChange,
    handleEndTimeChange,
  };
};
