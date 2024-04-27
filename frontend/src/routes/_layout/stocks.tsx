import {
  Container,
  Heading,
  Skeleton,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

import { Suspense } from "react";
import { ErrorBoundary } from "react-error-boundary";
import { StocksService } from "../../client";
import ActionsMenu from "../../components/Common/ActionsMenu";
import Navbar from "../../components/Common/Navbar";

export const Route = createFileRoute("/_layout/stocks")({
  component: Stocks,
});

function StocksTableBody() {
  const { data: stocks } = useSuspenseQuery({
    queryKey: ["stocks"],
    queryFn: () => StocksService.readStocks({}),
  });

  return (
    <Tbody>
      {stocks.data.map((stock) => (
        <Tr key={stock.id}>
          <Td>{stock.id}</Td>
          <Td>{stock.symbol}</Td>
          <Td>{stock.quantity}</Td>
          <Td>{stock.purchase_price.toFixed(2)}</Td>
          <Td>{stock.current_price ? stock.current_price.toFixed(2) : "N/A"}</Td>
          <Td>{new Date(stock.purchase_date).toLocaleDateString()}</Td>
          <Td>
            <ActionsMenu type={"Stock"} value={stock} />
          </Td>
        </Tr>
      ))}
    </Tbody>
  );
}

function StocksTable() {
  return (
    <TableContainer>
      <Table size={{ base: "sm", md: "md" }}>
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Symbol</Th>
            <Th>Quantity</Th>
            <Th>Purchase Price</Th>
            <Th>Current Price</Th>
            <Th>Purchase Date</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <ErrorBoundary
          fallbackRender={({ error }) => (
            <Tbody>
              <Tr>
                <Td colSpan={7}>Something went wrong: {error.message}</Td>
              </Tr>
            </Tbody>
          )}
        >
          <Suspense
            fallback={
              <Tbody>
                {new Array(5).fill(null).map((_, index) => (
                  <Tr key={index}>
                    {new Array(7).fill(null).map((_, index) => (
                      <Td key={index}>
                        <Skeleton height="20px" width="20px" />
                      </Td>
                    ))}
                  </Tr>
                ))}
              </Tbody>
            }
          >
            <StocksTableBody />
          </Suspense>
        </ErrorBoundary>
      </Table>
    </TableContainer>
  );
}

function Stocks() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Stocks Management
      </Heading>

      <Navbar type={"Stock"} />
      <StocksTable />
    </Container>
  );
}
