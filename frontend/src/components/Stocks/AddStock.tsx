import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    NumberInput,
    NumberInputField,
  } from "@chakra-ui/react";
  import { useMutation, useQueryClient } from "@tanstack/react-query";
  import { type SubmitHandler, useForm } from "react-hook-form";

  import { type ApiError, type StockCreate, StocksService } from "../../client";
  import useCustomToast from "../../hooks/useCustomToast";

  interface AddStockProps {
    isOpen: boolean;
    onClose: () => void;
  }

  const AddStock = ({ isOpen, onClose }: AddStockProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();
    const {
      register,
      handleSubmit,
      reset,
      formState: { errors, isSubmitting },
    } = useForm<StockCreate>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: {
        symbol: "",
        quantity: 1,
        purchase_price: 0,
        current_price: 0,
        purchase_date: new Date().toISOString().substring(0, 10), // Assuming date as string
      },
    });

    const mutation = useMutation({
      mutationFn: (data: StockCreate) =>
        StocksService.createStock({ requestBody: data }),
      onSuccess: () => {
        showToast("Success!", "Stock added successfully.", "success");
        reset();
        onClose();
      },
      onError: (err: ApiError) => {
        const errDetail = (err.body as any)?.detail;
        showToast("Something went wrong.", `${errDetail}`, "error");
      },
      onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ["stocks"] });
      },
    });

    const onSubmit: SubmitHandler<StockCreate> = (data) => {
      mutation.mutate(data);
    };

    return (
      <>
        <Modal
          isOpen={isOpen}
          onClose={onClose}
          size={{ base: "sm", md: "md" }}
          isCentered
        >
          <ModalOverlay />
          <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
            <ModalHeader>Add Stock</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <FormControl isRequired isInvalid={!!errors.symbol}>
                <FormLabel htmlFor="symbol">Symbol</FormLabel>
                <Input
                  id="symbol"
                  {...register("symbol", {
                    required: "Symbol is required.",
                  })}
                  placeholder="Stock Symbol"
                />
                {errors.symbol && (
                  <FormErrorMessage>{errors.symbol.message}</FormErrorMessage>
                )}
              </FormControl>

              <FormControl mt={4} isRequired isInvalid={!!errors.quantity}>
                <FormLabel htmlFor="quantity">Quantity</FormLabel>
                <NumberInput min={1}>
                  <NumberInputField
                    id="quantity"
                    {...register("quantity", {
                      required: "Quantity is required.",
                      valueAsNumber: true,
                    })}
                  />
                </NumberInput>
                {errors.quantity && (
                  <FormErrorMessage>{errors.quantity.message}</FormErrorMessage>
                )}
              </FormControl>

              <FormControl mt={4} isRequired isInvalid={!!errors.purchase_price}>
                <FormLabel htmlFor="purchase_price">Purchase Price</FormLabel>
                <NumberInput step={0.01}>
                  <NumberInputField
                    id="purchase_price"
                    {...register("purchase_price", {
                      required: "Purchase price is required.",
                      valueAsNumber: true,
                    })}
                  />
                </NumberInput>
                {errors.purchase_price && (
                  <FormErrorMessage>{errors.purchase_price.message}</FormErrorMessage>
                )}
              </FormControl>

              <FormControl mt={4}>
                <FormLabel htmlFor="current_price">Current Price</FormLabel>
                <NumberInput step={0.01}>
                  <NumberInputField
                    id="current_price"
                    {...register("current_price", {
                      valueAsNumber: true,
                    })}
                  />
                </NumberInput>
              </FormControl>

              <FormControl mt={4} isRequired isInvalid={!!errors.purchase_date}>
                <FormLabel htmlFor="purchase_date">Purchase Date</FormLabel>
                <Input
                  id="purchase_date"
                  type="date"
                  {...register("purchase_date", {
                    required: "Purchase date is required.",
                  })}
                />
                {errors.purchase_date && (
                  <FormErrorMessage>{errors.purchase_date.message}</FormErrorMessage>
                )}
              </FormControl>
            </ModalBody>

            <ModalFooter gap={3}>
              <Button variant="primary" type="submit" isLoading={isSubmitting}>
                Save
              </Button>
              <Button onClick={onClose}>Cancel</Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    );
  };

  export default AddStock;
