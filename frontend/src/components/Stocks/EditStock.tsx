import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    NumberInput,
    NumberInputField,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
  } from "@chakra-ui/react";
  import { useMutation, useQueryClient } from "@tanstack/react-query";
  import { type SubmitHandler, useForm } from "react-hook-form";
  
  import {
    type ApiError,
    type StockPublic,
    type StockUpdate,
    StocksService,
  } from "../../client";
  import useCustomToast from "../../hooks/useCustomToast";
  
  interface EditStockProps {
    stock: StockPublic;
    isOpen: boolean;
    onClose: () => void;
  }
  
  const EditStock = ({ stock, isOpen, onClose }: EditStockProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();
    const {
      register,
      handleSubmit,
      reset,
      formState: { isSubmitting, errors, isDirty },
    } = useForm<StockUpdate>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: stock,
    });
  
    const mutation = useMutation({
      mutationFn: (data: StockUpdate) =>
        StocksService.updateStock({ id: stock.id, requestBody: data }),
      onSuccess: () => {
        showToast("Success!", "Stock updated successfully.", "success");
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
  
    const onSubmit: SubmitHandler<StockUpdate> = async (data) => {
      mutation.mutate(data);
    };
  
    const onCancel = () => {
      reset();
      onClose();
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
            <ModalHeader>Edit Stock</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <FormControl isInvalid={!!errors.symbol}>
                <FormLabel htmlFor="symbol">Symbol</FormLabel>
                <Input
                  id="symbol"
                  {...register("symbol", {
                    required: "Symbol is required",
                  })}
                  type="text"
                />
                {errors.symbol && (
                  <FormErrorMessage>{errors.symbol.message}</FormErrorMessage>
                )}
              </FormControl>
              <FormControl mt={4} isInvalid={!!errors.quantity}>
                <FormLabel htmlFor="quantity">Quantity</FormLabel>
                <NumberInput min={0}>
                  <NumberInputField
                    id="quantity"
                    {...register("quantity", {
                      valueAsNumber: true,
                    })}
                  />
                </NumberInput>
                {errors.quantity && (
                  <FormErrorMessage>{errors.quantity.message}</FormErrorMessage>
                )}
              </FormControl>
              <FormControl mt={4} isInvalid={!!errors.purchase_price}>
                <FormLabel htmlFor="purchase_price">Purchase Price</FormLabel>
                <NumberInput precision={2} step={0.01}>
                  <NumberInputField
                    id="purchase_price"
                    {...register("purchase_price", {
                      valueAsNumber: true,
                    })}
                  />
                </NumberInput>
                {errors.purchase_price && (
                  <FormErrorMessage>{errors.purchase_price.message}</FormErrorMessage>
                )}
              </FormControl>
              <FormControl mt={4} isInvalid={!!errors.current_price}>
                <FormLabel htmlFor="current_price">Current Price</FormLabel>
                <NumberInput precision={2} step={0.01}>
                  <NumberInputField
                    id="current_price"
                    {...register("current_price", {
                      valueAsNumber: true,
                    })}
                  />
                </NumberInput>
                {errors.current_price && (
                  <FormErrorMessage>{errors.current_price.message}</FormErrorMessage>
                )}
              </FormControl>
              <FormControl mt={4} isInvalid={!!errors.purchase_date}>
                <FormLabel htmlFor="purchase_date">Purchase Date</FormLabel>
                <Input
                  id="purchase_date"
                  {...register("purchase_date", {
                    required: "Purchase date is required.",
                  })}
                  type="date"
                />
                {errors.purchase_date && (
                  <FormErrorMessage>{errors.purchase_date.message}</FormErrorMessage>
                )}
              </FormControl>
            </ModalBody>
            <ModalFooter gap={3}>
              <Button
                variant="primary"
                type="submit"
                isLoading={isSubmitting}
                isDisabled={!isDirty}
              >
                Save
              </Button>
              <Button onClick={onCancel}>Cancel</Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </>
    );
  };
  
  export default EditStock;
  